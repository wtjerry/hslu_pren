class Encoder(object):
    def position(self, x, y):
        COMMAND_ID = 2
        command_id_enc = self.__encode_utf8(COMMAND_ID)

        x_enc = self.__encode_utf8(x)
        y_enc = self.__encode_utf8(y)

        COMMAND_ID_CHAR_LENGTH = 1
        length = COMMAND_ID_CHAR_LENGTH + len(x_enc) + len(y_enc)
        len_enc = self.__encode_utf8("{num:05d}".format(num=length))

        return len_enc + command_id_enc + x_enc + y_enc

    def __encode_utf8(self, i):
        return str(i).encode("utf8")
