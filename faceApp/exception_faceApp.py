class NotFoundFace(Exception):

    def __str__(self):
        return "WARNING: No faces found.";


class MoreThanOneFaceFound(Exception):
    def __str__(self):
        return "WARNING: More than one face found.";
