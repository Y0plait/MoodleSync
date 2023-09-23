"""

Filename: MoodleSyncExtras.py
Author: Anton Moulin
Date : 23/09/2023

Abstract:
    Miscallenous classes & methods for error handling and parameters. Used in MoodleSyncMain.py
"""

class ExportParams:

    class Duration():
        CURRENT_WEEK="weeknow"
        NEXT_WEEK="weeknext"
        MONT_NOW="monthnow"
        NEXT_SIXTY_DAY="recentupcoming"

    class Events():
        ALL="all"
        CATEGORIES_RELATED="categories"
        CLASSES_RELATED= "courses"
        GROUPS_RELATED="groupes"
        PERSONNAL="user"

class MoodleLoginError(Exception):
    pass