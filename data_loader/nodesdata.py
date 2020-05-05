import numpy as np

class Nodes(object):
    def __init__(self):
        self.dictBook=dict()

    def nodesdict(self):
        labels={}
        self.dictBook.setdefault(1, np.array([80.3188, 28.9819]))
        labels[1] = r'$Mahendra Nagar$'
        self.dictBook.setdefault(2, np.array([80.4723, 29.2615]))
        labels[2] = r'$Baitadi$'
        self.dictBook.setdefault(3, np.array([80.7875, 29.7863]))
        labels[3] = r'$Darchula$'
        self.dictBook.setdefault(4, np.array([80.6168, 28.8386]))
        labels[4] = r'$Dhangadi$'
        self.dictBook.setdefault(5, np.array([81.0896, 29.2765]))
        labels[5] = r'$Doti$'
        self.dictBook.setdefault(6, np.array([81.4836, 29.5837]))
        labels[6] = r'$Bajhang$'
        self.dictBook.setdefault(7, np.array([81.523, 29.3288]))
        labels[7] = r'$Sanfe Bagar$'
        self.dictBook.setdefault(8, np.array([82.3767, 29.4465]))
        labels[8] = r'$Bajura$'
        self.dictBook.setdefault(9, np.array([81.1027, 29.6033]))
        labels[9] = r'$Tikapur$'
        self.dictBook.setdefault(10, np.array([81.9177, 29.9955]))
        labels[10] = r'$Simikot$'
        self.dictBook.setdefault(11, np.array([81.6544, 28.9563]))
        labels[11] = r'$Surkhet$'
        self.dictBook.setdefault(12, np.array([81.4442, 28.4007]))
        labels[12] = r'$Nepalgunj$'
        self.dictBook.setdefault(13, np.array([82.4424, 29.0674]))
        labels[13] = r'$Jumla$'
        self.dictBook.setdefault(14, np.array([82.0878, 28.7929]))
        labels[14] = r'$Chaurjhari$'
        self.dictBook.setdefault(15, np.array([81.8645, 28.4138]))
        labels[15] = r'$Dang$'
        self.dictBook.setdefault(16, np.array([82.2191, 28.6621]))
        labels[16] = r'$Salle$'
        self.dictBook.setdefault(17, np.array([83.2173, 28.8451]))
        labels[17] = r'$Dolpa$'
        self.dictBook.setdefault(18, np.array([83.7952, 28.7144]))
        labels[18] = r'$Jomsom$'
        self.dictBook.setdefault(19, np.array([82.6263, 27.9432]))
        labels[19] = r'$Bhairawa$'
        self.dictBook.setdefault(20, np.array([83.677, 28.27]))
        labels[20] = r'$Pokhara$'
        self.dictBook.setdefault(21, np.array([83.9134, 28.6491]))
        labels[21] = r'$Manang$'
        self.dictBook.setdefault(22, np.array([84.1761, 27.5968]))
        labels[22] = r'$Mehgauli$'
        self.dictBook.setdefault(23, np.array([84.36, 27.636]))
        labels[23] = r'$Bharatpur$'
        self.dictBook.setdefault(24, np.array([85.0955, 27.1458]))
        labels[24] = r'$Simara$'
        self.dictBook.setdefault(25, np.array([85.1743, 27.7405]))
        labels[25] = r'$Kathmandu$'
        self.dictBook.setdefault(26, np.array([85.9361, 26.7928]))
        labels[26] = r'$Janakpur$'
        self.dictBook.setdefault(27, np.array([85.9361, 27.3615]))
        labels[27] = r'$Ramechap$'
        self.dictBook.setdefault(28, np.array([86.1987, 27.4007]))
        labels[28] = r'$Rumjatar$'
        self.dictBook.setdefault(29, np.array([86.2119, 27.551]))
        labels[29] = r'$Phaplu$'
        self.dictBook.setdefault(30, np.array([86.3957, 27.3157]))
        labels[30] = r'$Lamidanda$'
        self.dictBook.setdefault(31, np.array([86.3563, 26.7078]))
        labels[31] = r'$Rajbiraj$'
        self.dictBook.setdefault(32, np.array([86.8817, 27.6425]))
        labels[32] = r'$Lukla$'
        self.dictBook.setdefault(33, np.array([87.0918, 27.7013]))
        labels[33] = r'$Syangboche$'
        self.dictBook.setdefault(34, np.array([86.7372, 27.2111]))
        labels[34] = r'$Bhojpur$'
        self.dictBook.setdefault(35, np.array([86.9211, 27.3157]))
        labels[35] = r'$Tumlingtar$'
        self.dictBook.setdefault(36, np.array([87.2757, 26.5248]))
        labels[36] = r'$Biratnagar$'
        self.dictBook.setdefault(37, np.array([87.5515, 27.5052]))
        labels[37] = r'$Taplegunj$'
        self.dictBook.setdefault(38, np.array([87.8273, 26.6556]))
        labels[38] = r'$Bhadrapur$'

        coord = self.dictBook
        return coord, labels

