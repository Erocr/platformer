from Collisions.Hitbox import *
from Collisions.CollisionInfo import *


class CollisionAnalyzer:
    """ This class will analyze the results of the collisions functions, in order to give more readable information """
    def __init__(self, hitboxes: list[Hitbox]):
        self.hitboxes = hitboxes


# Hitbox management ----------------------------------------------------------------------------------------------------

    def add_hitbox(self, hitbox):
        self.hitboxes.append(hitbox)

    def remove_hitbox(self, hitbox):
        self.hitboxes.remove(hitbox)

# Analyzing functions --------------------------------------------------------------------------------------------------

    def collision_infos(self) -> list[CollisionInfo]:
        """
        :return: the hitboxes with which he has a collision
        """
        res = []
        for hitbox in self.hitboxes:
            res += hitbox.collisionInfos
        return res

    def has_collision(self) -> bool:
        """ If he is in collision with something """
        return len(self.collision_infos()) > 0

    def touch_floor(self):
        """ Returns None if he doesn't touch any floor. The floor if he touches a floor """
        # TODO: it considers as floor if he bonks his head
        for coll_info in self.collision_infos():
            if abs(coll_info.tangent.x) > abs(coll_info.tangent.y):
                return coll_info.hitbox
        return None
