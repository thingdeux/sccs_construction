import sys

#Logger to write to stderr
def log(message, severity="ERROR"):
    sys.stderr.write(str(severity) + " - " + str(message) + "\n")    