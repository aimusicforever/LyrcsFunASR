def secendToHMS(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    hms = "%02d:%02d:%02d" % (h, m, s)
    return hms


# LRC的时间标签的格式为[mm:ss.xx]其中mm为分钟数、ss为秒数、xx为百分之一秒
def secendToLyc
(millon_seconds):
    seconds, leftMillonSeconds = divmod(millon_seconds, 1000)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    hundredSecond, ms = divmod(leftMillonSeconds, 10)
    hms = "%02d:%02d.%02d" % (m, s, hundredSecond)
    return hms