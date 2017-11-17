class Decoder(object):
    def decode(self, data):
        length = int(data[:5])
        self.raise_if_not_correct_length(data, length)
        command_id = int(data[5:6].decode("utf8"))
        parameter = data[6:-1].decode("utf8")
        return command_id, parameter

    def raise_if_not_correct_length(self, data, length):
        NEWLINE_CHAR_LENGTH = 1
        expected_total_length = length + 5 + NEWLINE_CHAR_LENGTH
        actual_total_length = len(data)
        if not actual_total_length == expected_total_length:
            error_message = "received data is of not expected length. Expected: {0}, actual: {1}, data: {2}." \
                .format(expected_total_length, actual_total_length, data)
            raise ValueError(error_message)
