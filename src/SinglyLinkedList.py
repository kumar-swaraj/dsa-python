from dataclasses import dataclass
from typing import Generic, TypeVar, Optional, Iterator

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    value: T
    next: Optional["Node[T]"] = None


class SinglyLinkedListIterator(Iterator[T]):
    def __init__(self, head: Optional[Node[T]]) -> None:
        self.current = head

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self.current is None:
            raise StopIteration
        value = self.current.value
        self.current = self.current.next
        return value


class SinglyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self._length: int = 0

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator[T]:
        return SinglyLinkedListIterator[T](self.head)

    # Time: O(1) | Space: O(1)
    def append(self, value: T) -> "SinglyLinkedList[T]":
        new_node = Node(value)

        if self.head is None or self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node

        self.tail = new_node

        self._length += 1
        return self

    # Time: O(1) | Space: O(1)
    def prepend(self, value: T) -> "SinglyLinkedList[T]":
        new_node = Node(value, next=self.head)

        if self.tail is None:
            self.tail = new_node

        self.head = new_node
        self._length += 1
        return self

    # Time: O(n) | Space: O(1)
    def remove_last(self) -> T:
        if self.head is None or self.tail is None:
            raise IndexError("List is empty.")

        last_value = self.tail.value

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            current = self.head
            while current.next is not None and current.next != self.tail:
                current = current.next
            current.next = None
            self.tail = current

        self._length -= 1
        return last_value

    # Time: O(1) | Space: O(1)
    def remove_first(self) -> T:
        if self.head is None or self.tail is None:
            raise IndexError("List is empty.")

        first_value = self.head.value
        self.head = self.head.next
        if not self.head:
            self.tail = None

        self._length -= 1
        return first_value

    # Time: O(n) | Space: O(1)
    def remove(self, value: T) -> T:
        if self.head is None or self.tail is None:
            raise IndexError("List is empty.")

        if self.head.value == value:
            return self.remove_first()

        previous_node = self.head
        current_node = self.head.next

        while current_node is not None and current_node.value != value:
            previous_node = current_node
            current_node = current_node.next

        if current_node is None:
            raise ValueError("Item not in list.")

        if current_node.next is None:
            self.tail = previous_node

        previous_node.next = current_node.next
        current_node.next = None

        self._length -= 1
        return current_node.value

    # Time: O(n) | Space: O(1)
    def reverse(self) -> "SinglyLinkedList[T]":
        if self._length < 2 or self.head is None or self.tail is None:
            return self

        left_node: Optional[Node[T]] = None
        middle_node: Optional[Node[T]] = self.head

        while middle_node is not None:
            right_node: Optional[Node[T]] = middle_node.next
            middle_node.next = left_node
            left_node = middle_node
            middle_node = right_node

        self.head, self.tail = self.tail, self.head
        return self
