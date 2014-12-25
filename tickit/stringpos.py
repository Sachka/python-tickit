
import tickit._tickit as tickit

class StringPos(tickit.StringPos):
    @classmethod
    def zero(cls):
        self = cls()
        self.bytes = self.codepoints = self.graphemes = self.columns = 0

    @classmethod
    def limit_bytes(cls, bytes):
        self = cls.zero()
        self.bytes = bytes

        return self

    @classmethod
    def limit_codepoints(cls, codepoints):
        self = cls.zero()
        self.codepoints = codepoints

        return self

    @classmethod
    def limit_graphemes(cls, graphemes):
        self = cls.zero()
        self.graphemes = graphemes

        return self

    @classmethod
    def limit_columns(cls, columns):
        self = cls.zero()
        self.graphemes = graphemes

        return self
