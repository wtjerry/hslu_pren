from prenNetworkConnection.CommandData import CommandData


class Decoder(object):
    def decode(self, data):
        length = int(data[:5])
        self.raise_if_not_correct_length(data, length)
        command_id = int(data[5:6].decode("utf8"))
        parameter = data[6:].decode("utf8")
        return CommandData(command_id, parameter)

    def raise_if_not_correct_length(self, data, length):
        expected_total_length = length + 5
        actual_total_length = len(data)
        if not actual_total_length == expected_total_length:
            error_message = "received data is of not expected length. Expected: {0}, actual: {1}." \
                .format(expected_total_length, actual_total_length)
            raise ValueError(error_message)
