import math


class Math:

    @staticmethod
    def normalize_vector(vector):
        if vector == [0, 0]:
            return [0, 0]
        pythagoras = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
        return vector[0] / pythagoras, vector[1] / pythagoras

    @staticmethod
    def rotate_vector(vector, theta):
        result = (vector[0] * math.cos(theta)
                  - vector[1] * math.sin(theta),
                  vector[0] * math.sin(theta)
                  + vector[1] * math.cos(theta))
        return result

    @staticmethod
    def add_vectors(vector1, vector2):
        return vector1[0] + vector2[0], vector1[1] + vector2[1]
    
    @staticmethod
    def subtract_vectors(vector1, vector2):
        return vector1[0] - vector2[0], vector1[1] - vector2[1]

    @staticmethod
    def multiply_vector(vector, multiplier):
        return vector[0] * multiplier, vector[1] * multiplier

    @staticmethod
    def vector_length(vector):
        return math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])

    @staticmethod
    def vector_distance(vector1, vector2):
        return Math.vector_length(Math.subtract_vectors(vector1, vector2))
