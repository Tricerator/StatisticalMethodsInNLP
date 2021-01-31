import matplotlib.pyplot as plt

with open("TEXTCZ1RESULTS.txt", "r") as cs:
    linesCZ = []
    for line in cs.readlines():
        if line.startswith("M:"):
            linesCZ.append(line)
    with open("TEXTEN1RESULTS.txt", "r") as en:
        linesEN = []
        for line in en.readlines():
            if line.startswith("M:"):
                linesEN.append(line)
        with open("TEXTOBARESULTS.txt", "r") as both:
            linesBoth = []
            for line in both.readlines():
                if line.startswith("M:"):
                    linesBoth.append(line)

            x = []
            y1 = []
            y2 = []
            y3 = []
            y4 = []
            y5 = []
            y6 = []
            for char in ["E", "P", "WC", "NCPW", "BF", "UF"]:
                if char == "E":
                    name = "Entropy"
                elif char == "P":
                    name = "Perplexity"
                elif char == "WC":
                    name = "Number of words"
                elif char == "NCPW":
                    name = "Number of chars per word"
                elif char == "BF":
                    name = "Biggest frequency"
                elif char == "UF":
                    name = "Unique words in text"

                for mess in ["words", "characters"]:

                    for i in linesCZ:
                        data = i.split(":")
                        if not data[1] in x:
                            x.append(data[1])
                        if char == data[2]:
                            if data[3] == "words" and float(data[5]) not in y1:
                                y1.append(float(data[5]))
                            elif data[3] == "characters" and float(data[5]) not in y2:
                                y2.append(float(data[5]))

                    for j in linesEN:
                        data = j.split(":")
                        if char == data[2]:
                            if data[3] == "words" and float(data[5]) not in y3:
                                y3.append(float(data[5]))
                            elif data[3] == "characters" and float(data[5]) not in y4:
                                y4.append(float(data[5]))
                    for k in linesBoth:
                        data = k.split(":")
                        if char == data[2]:
                            if data[3] == "words" and float(data[5]) not in y5:
                                y5.append(float(data[5]))
                            elif data[3] == "characters" and float(data[5]) not in y6:
                                y6.append(float(data[5]))

                # The data are in opposite direction
                x = x[::-1]
                y1 = y1[::-1]
                y2 = y2[::-1]
                y3 = y3[::-1]
                y4 = y4[::-1]
                y5 = y5[::-1]
                y6 = y6[::-1]

                print(name)
                print(x, "\n", y1, "\n", y2, "\n", y3, "\n", y4,"\n", y5, "\n", y6)
                print(len(x), len(y1), len(y2), len(y3), len(y4), len(y5), len(y6))
                if (len(x) == len(y1) and len(x) == len(y2) and len(x) == len(y3) and len(x) == len(y4)):
                    plt.plot(x, y1, color="green", label="CZ words")
                    plt.xlabel('messUp probability')
                    plt.ylabel(name)
                    plt.plot(x, y2, color="blue", label="CZ characters")
                    plt.plot(x, y3, color="yellow", label="EN words")
                    plt.plot(x, y4, color="red", label="EN characters")
                    plt.plot(x, y5, color="orange", label="Both words")
                    plt.plot(x, y6, color="black", label="Both characters")
                    plt.legend()
                    plt.savefig(name + ".png")
                x = []
                y1 = []
                y2 = []
                y3 = []
                y4 = []
                y5 = []
                y6 = []

                plt.clf()
                plt.cla()
