import io

import cv2
import math
import numpy as np
import picamera
from picamera.array import PiRGBArray
from time import sleep
from datetime import datetime


def print_time(text):
    print("{time}: {text}".format(time=datetime.now(), text=text))


def print_elapsed_time(func, *p):
    before = datetime.now()
    result = func(*p)
    after = datetime.now()
    diff = after - before
    caller_function_name = func.__name__
    print("'{func}' took {time}".format(func=caller_function_name, time=diff))
    return result


class GoalDetection(object):
    _camera = None

    _INNERMOST_SQUARE_HEIGHT_CM = 6.0
    _GRAY_THRESHOLD = 100
    _MIN_SQUARE_AREA_RATIO = 0.005  # 0.5% of the image
    _MAX_SQUARE_AREA_RATIO = 0.950  # 95% of the image
    _MIN_SQUARE_XY_RATIO = 0.85
    _MAX_SQUARE_XY_RATIO = 1.15
    _MAX_PERIMETER_DELTA_RATIO = 0.1

    @staticmethod
    def determine_center(contours):
        cx, cy = -1, -1
        m = cv2.moments(contours)
        m00 = m['m00']
        if m00 > 0:
            cx = int(m['m10'] / m00)
            cy = int(m['m01'] / m00)
        return cx, cy

    def find_threshold(self, image):
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blurred = cv2.blur(image_gray, (5, 5))
        threshold = cv2.threshold(blurred, self._GRAY_THRESHOLD, 255, cv2.THRESH_BINARY)
        return threshold

    def is_square_shaped(self, contours):
        peri = cv2.arcLength(contours, True)
        approx = cv2.approxPolyDP(contours, self._MAX_PERIMETER_DELTA_RATIO * peri, True)
        if len(approx) != 4:
            return False
        (x, y, w, h) = cv2.boundingRect(approx)
        width_height_ratio = w / float(h)
        sensible_width_height_ratio = (self._MAX_SQUARE_XY_RATIO > width_height_ratio > self._MIN_SQUARE_XY_RATIO)

        # L-shaped areas are also polygons, but have a much smaller area
        square_area_px = cv2.contourArea(contours)
        max_area = w * self._MAX_SQUARE_XY_RATIO * h * self._MAX_SQUARE_XY_RATIO
        min_area = w * self._MIN_SQUARE_XY_RATIO * h * self._MIN_SQUARE_XY_RATIO
        sensible_area = (max_area > square_area_px > min_area)

        return sensible_width_height_ratio and sensible_area

    def estimate_distance_to_center(self, image, contours):
        h, _, _ = image.shape
        perimeter = cv2.arcLength(contours, True)
        innermost_square_height_px = perimeter / 4.0
        cm_in_pixels = innermost_square_height_px / self._INNERMOST_SQUARE_HEIGHT_CM
        _, cy = self.determine_center(contours)
        dist_px = h / 2 - cy
        dist_cm = dist_px / cm_in_pixels
        return int(dist_px), dist_cm

    def has_square_area(self, image, contours):
        h, w, _ = image.shape
        square_area_px = cv2.contourArea(contours)
        image_area_px = w * h
        min = self._MIN_SQUARE_AREA_RATIO * image_area_px
        max = self._MAX_SQUARE_AREA_RATIO * image_area_px
        return max > square_area_px > min

    def has_neighbours(self, hierarchy):
        return hierarchy[0] != -1 or hierarchy[1] != -1

    def classify(self, cont_hier_list):
        min_area, max_area = math.inf, -1
        min_cont, max_cont = None, None
        others = []
        for item in cont_hier_list:
            cont = item[0]
            hier = item[1]
            area = cv2.contourArea(cont)
            if area < min_area and hier[2] == -1 and hier[3] != -1:
                min_area = area
                min_cont = cont
            if area > max_area and hier[2] != -1:
                max_area = area
                max_cont = cont

        for item in cont_hier_list:
            cont = item[0]
            is_min = np.array_equal(cont, min_cont)
            is_max = np.array_equal(cont, max_cont)
            if not is_min and not is_max:
                others.append(cont)

        return min_cont, max_cont, others

    def calc_middle(self, image):
        h, _, _ = image.shape
        middle = int(h / 2)
        return middle

    def process(self, img, queue):
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        threshold = self.find_threshold(image_rgb)[1]

        _, contours, hierarchy = cv2.findContours(threshold.copy(),
                                                  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        square_candidates = []
        for item in zip(contours, hierarchy[0]):
            cont = item[0]
            hier = item[1]
            if self.has_neighbours(hier):
                continue
            if not self.has_square_area(image_rgb, cont):
                continue
            if not self.is_square_shaped(cont):
                continue
            square_candidates.append((cont, hier))

        smallest, biggest, others = self.classify(square_candidates)
        if smallest is not None:
            (cx, cy) = self.determine_center(smallest)
            dist_px, dist_cm = self.estimate_distance_to_center(image_rgb, smallest)
            dist_mm = dist_cm * 10
            print_time('distance: {:4d}px {:7.3f}cm'.format(dist_px, dist_cm))
            if cx > 0 and cy > 0:
                h, _, _ = image_rgb.shape
                queue.put(dist_mm)
                if h * 0.5 > dist_px >= h * 0.3:
                    print_time('far away: {:.3f}cm'.format(dist_cm))
                elif h * 0.3 > dist_px >= h * 0.2:
                    print_time('away: {:.3f}cm'.format(dist_cm))
                elif h * 0.2 > dist_px >= h * 0.1:
                    print_time('close: {:.3f}cm'.format(dist_cm))
                elif h * 0.1 > dist_px >= h * 0.05:
                    print_time('closer: {:.3f}cm'.format(dist_cm))
                elif h * 0.05 > dist_px >= h * 0.01:
                    print_time('very close: {:.3f}cm'.format(dist_cm))
                elif h * 0.01 > dist_px >= 0:
                    print_time('extremely close: {:.3f}cm'.format(dist_cm))
                elif dist_px < 0:
                    print_time('passed: {:.3f}cm'.format(dist_cm))
                elif dist_px > 0:
                    print_time('way too far away')
                else:
                    print_time('unknown distance')

    def start(self, queue):
        self._camera = picamera.PiCamera()
        self._camera.resolution = (1920, 1080)
        rawCapture = PiRGBArray(self._camera, size=(1920, 1080))
        sleep(0.1)
        for frame in self._camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            print_elapsed_time(self.process, frame.array, queue)
            rawCapture.truncate(0)
