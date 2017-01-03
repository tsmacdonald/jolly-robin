import random, sys

MELODIC_JUMP = 7

NOTES = [
  'A,',
  'B,', 'C', 'D', 'E', 'F', 'G', 'A',
  'B',  'c', 'd', 'e', 'f', 'g', 'a',
  'b']

class Tune():
    def __init__(self, notes):
        def straight(a, b):
            return NOTES[a] + NOTES[b]
        def birl(a, b):
            return (NOTES[a] + '/' +
                    NOTES[a] + '/' +
                    NOTES[a] + ' ')
        def triplet(a, b):
            return "(3 %s%s%s"%(NOTES[a], NOTES[int((a + b) / 2)], NOTES[b])
        self.notes = notes
        self.rhythms = [straight] * 17 + [birl] * 2 + [triplet]
        self.fudge = [-1, 0, 0, 0, 1]

    def __a_note(self, last_note, should_fudge=False):
        fudge = self.fudge if should_fudge else [0]
        if last_note is None:
            note = self.__fudged_note(random.choice(self.notes), fudge)
            self.last_note = note
            return note
        note = -MELODIC_JUMP * 2
        while abs(note - last_note) > MELODIC_JUMP:
            note = self.__fudged_note(random.choice(self.notes), fudge)
        self.last_note = note
        return note

    def __fudged_note(self, note, fudge):
        adjustment = random.choice(fudge)
        if adjustment == 0:
            return note
        candidate = self.last_note + adjustment
        if candidate > len(self.notes):
            return note
        return candidate


    def generate(self, last_note):
        self.last_note = last_note
        a = self.__a_note(last_note)
        b = self.__a_note(a, True)
        c = self.__a_note(b)
        d = self.__a_note(c, True)
        return (random.choice(self.rhythms)(a, b) +
                random.choice(self.rhythms)(c, d) + ' ')

class SP1():
    def __init__(self):
        self.last_note = 12

    def generate(self, _):
        return "fgaf "

class SP2():
    def __init__(self):
        self.last_note = 11

    def generate(self, _):
        return "eAce "


def generate_header():
    return """
%%barsperstaff 4
X:1
T:Jolly Robin
C:THE MACHINE
M:C|
L:1/8
K:Bm
"""


def main(out_file, times):
    A = Tune([0, 2, 4, 7, 7, 7, 9, 9, 11, 11, 14, 14])
    B = Tune([1, 3, 5, 8, 8, 8, 10, 10, 12, 12, 15, 15])
    form = [B, B, B, A,
            B, B, SP1(), SP2()]
    output = generate_header()
    last_note = None
    for time in xrange(times):
        for i, chord in enumerate(form):
            output += chord.generate(last_note)
            last_note = chord.last_note
            if i % 2 == 1:
                output += '| '
    with open(out_file, 'w') as f:
        f.write(output)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
