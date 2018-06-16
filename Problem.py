# id: 640;Stairs
# title:"Schody",
# about:"",
# robotCol:3,
# robotRow:10,
# robotDir:3,
# subs:[3,3,0,0,0],
# allowedCommands:0,
# board:"                   ggggggggGG      gggggggGGg      ggggggGGgg      gggggGGggg      ggggGGgggg      gggGGggggg      ggGGgggggg      gGGggggggg      GGgggggggg      gggggggggg                   "


class Problem: 
    def __init__(self, parse_str):
        gen = self.__lineGenerator(parse_str)

        self.id = next(gen)
        self.title = next(gen)
        self.about = next(gen)
        self.robotCol = (int)(next(gen))
        self.robotRow = (int)(next(gen))
        self.robotDir = (int)(next(gen))
        self.subs = next(gen)
        self.allowedCommands = (int)(next(gen))

        self.board_str = next(gen)

    def getBoardCopy(self):
        arr = [self.board_str[i:i+16] for i in range(0, 16*12, 16)]

        return arr

    def getFlowerCount(self):
        return self.board_str.count("R") + self.board_str.count("G") + self.board_str.count("B")

    def getFirstId(self):
        arr = self.id.split(';')

        if len(arr) == 1:
            return self.id.zfill(4)
        else:
            return arr[0].zfill(4)

    def __lineGenerator(self, parse_str):
        for line in parse_str.splitlines():
            if len(line) == 0:
                continue

            line = line.strip()

            if line[-1] == ',':
                line = line[:-1]
            
            arr = line.split(':')

            yield arr[1].strip().replace('"', "")
