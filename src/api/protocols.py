from typing import List

# from src.user.models import UserResponseV1, UserAddRequestV1
from src.post.models import PostResponseV1, PostRequestV1, PostUpdateRequestV1


# class UserServiceProtocol:
#     def get_all(self) -> List[UserResponseV1]:
#         raise NotImplementedError
#
#     def get_one(self, id: int) -> UserResponseV1:
#         raise NotImplementedError
#
#     def create(self, user: UserAddRequestV1) -> None:
#         raise NotImplementedError
#
#     def delete(self, id: int) -> None:
#         raise NotImplementedError


class PostServiceProtocol:
    def get_all(self) -> List[PostResponseV1]:
        raise NotImplementedError

    def get_one(self, id: int) -> PostResponseV1:
        raise NotImplementedError

    def create(self, user: PostRequestV1) -> None:
        raise NotImplementedError

    def update(self, id: int, user: PostUpdateRequestV1) -> None:
        raise NotImplementedError

    def delete(self, id: int) -> None:
        raise NotImplementedError

    def get_stats_by_user_id(self, id: int, date_from, date_to) -> PostResponseV1:
        raise NotImplementedError
