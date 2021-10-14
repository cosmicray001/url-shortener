class Encode:

    def base62_encode(self, md_five_hash):
        """
        Convert md5 hash to base62
        Arguments:
        - `md_five_hash`: The md5 hash(string)
        doc: https://stackoverflow.com/a/1119769/16163845
        """
        md_five_hash = self.string_to_long(md_five_hash)
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if md_five_hash == 0:
            return alphabet[0]
        arr = []
        arr_append = arr.append  # Extract bound-method for faster access.
        _divmod = divmod  # Access to locals is faster.
        base = len(alphabet)
        while md_five_hash:
            md_five_hash, rem = _divmod(md_five_hash, base)
            arr_append(alphabet[rem])
        arr.reverse()
        result = ''.join(arr)
        return result[:8]

    @staticmethod
    def string_to_long(md_five_hash):
        """
        This function takes a long string. Then converts it to long_int then return.
        :param md_five_hash: a long string
        :return: long_num
        """
        md5_hash = int(md_five_hash, 16)
        return md5_hash
