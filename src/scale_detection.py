# Scale detection, weight algos

# !pip install py-midi
# import midi
import math


class noteSet:
    def __init__(self):
        self.closestScale = ""
        self.noteAmounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.keys = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        self.modes = ["Major", "Minor"]

        # chromatic scales ascending, ordered by modes: major, minor, more to be added...
        # weight info: *2 for dominant, *1 for other in-scale tones, *0 for non-scale tones
        self.scaleWeights = [[2, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                             [1, 2, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
                             [0, 1, 2, 0, 1, 0, 1, 1, 0, 1, 0, 1],
                             [1, 0, 1, 2, 0, 1, 0, 1, 1, 0, 1, 0],
                             [0, 1, 0, 1, 2, 0, 1, 0, 1, 1, 0, 1],
                             [1, 0, 1, 0, 1, 2, 0, 1, 0, 1, 1, 0],
                             [0, 1, 0, 1, 0, 1, 2, 0, 1, 0, 1, 1],
                             [1, 0, 1, 0, 1, 0, 1, 2, 0, 1, 0, 1],
                             [1, 1, 0, 1, 0, 1, 0, 1, 2, 0, 1, 0],
                             [0, 1, 1, 0, 1, 0, 1, 0, 1, 2, 0, 1],
                             [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 2, 0],
                             [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 2],
                             [2, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
                             [0, 2, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                             [1, 0, 2, 0, 1, 1, 0, 1, 0, 1, 1, 0],
                             [0, 1, 0, 2, 0, 1, 1, 0, 1, 0, 1, 1],
                             [1, 0, 1, 0, 2, 0, 1, 1, 0, 1, 0, 1],
                             [1, 1, 0, 1, 0, 2, 0, 1, 1, 0, 1, 0],
                             [0, 1, 1, 0, 1, 0, 2, 0, 1, 1, 0, 1],
                             [1, 0, 1, 1, 0, 1, 0, 2, 0, 1, 1, 0],
                             [0, 1, 0, 1, 1, 0, 1, 0, 2, 0, 1, 1],
                             [1, 0, 1, 0, 1, 1, 0, 1, 0, 2, 0, 1],
                             [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 2, 0],
                             [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 2]]

    def setNoteAmounts(self, notes):
        for note in notes:
            noteMod = note % 12
            self.noteAmounts[noteMod] += 1

    def setScaleByIdx(self, scaleIdx):
        scaleKey = ""
        scaleMode = ""

        # Find scale key
        scaleKeyIdx = scaleIdx % 12
        scaleKey = n.keys[scaleKeyIdx]

        # Find scale mode
        scaleModeIdx = math.floor(scaleIdx / 12)
        scaleMode = n.modes[scaleModeIdx]

        self.closestScale = scaleKey + " " + scaleMode

    def findClosestScale(self):
        maxWeight = -1
        closestScaleIdx = -1
        candidateWeightMatrix = [[note * noteWeight for note, noteWeight in zip(self.noteAmounts, self.scaleWeights[i])]
                                 for i in range(len(self.scaleWeights))]

        for idx in range(len(candidateWeightMatrix)):
            candidateWeight = sum(candidateWeightMatrix[idx])
            if maxWeight < candidateWeight:
                maxWeight = candidateWeight
                closestScaleIdx = idx

        self.setScaleByIdx(closestScaleIdx)

        # return maxWeight, closestScaleIdx

    def showNoteValues(self):
        print("C: ", self.noteAmounts[0])
        print("Df:", self.noteAmounts[1])
        print("D: ", self.noteAmounts[2])
        print("Ef:", self.noteAmounts[3])
        print("E: ", self.noteAmounts[4])
        print("F: ", self.noteAmounts[5])
        print("Gf:", self.noteAmounts[6])
        print("G: ", self.noteAmounts[7])
        print("Af:", self.noteAmounts[8])
        print("A: ", self.noteAmounts[9])
        print("Bf:", self.noteAmounts[10])
        print("B: ", self.noteAmounts[11])


# MAIN
# notes set may be maintained as queue of a specific size (adding/removing notes one at a time)
notes = [60, 60, 62, 63, 65, 67]
n = noteSet()
n.setNoteAmounts(notes)

n.findClosestScale()
print(n.closestScale)