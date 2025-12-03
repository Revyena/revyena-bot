import math

BASE_XP = 100

class LevelingUtilities:
    @staticmethod
    def calculate_experience(level: int) -> int:
        return level ** 2 * BASE_XP

    @staticmethod
    def level_from_xp(xp: int) -> int:
        return int(math.sqrt(xp / BASE_XP))

    @staticmethod
    def progress_to_next_level(xp: int) -> float:
        level = LevelingUtilities.level_from_xp(xp)
        xp_current = LevelingUtilities.calculate_experience(level)
        xp_next = LevelingUtilities.calculate_experience(level + 1)
        return (xp - xp_current) / (xp_next - xp_current)
