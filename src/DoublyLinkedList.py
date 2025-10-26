from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    value: T
    previous: Optional["Node[T]"] = None
    next: Optional["Node[T]"] = None


class DoublyLinkedListIterator(Iterator[T]):
    def __init__(self, head: Optional[Node[T]]):
        self.current_node = head

    def __iter__(self):
        return self

    def __next__(self) -> T:
        if self.current_node is None:
            raise StopIteration
        else:
            current_value = self.current_node.value
            self.current_node = self.current_node.next
            return current_value


class DoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self._length: int = 0

    def __len__(self):
        return self._length

    def __iter__(self):
        return DoublyLinkedListIterator[T](self.head)

    # Time: O(1) | Space: O(1)
    def append(self, value: T) -> DoublyLinkedList[T]:
        new_node = Node(value, previous=self.tail)

        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self._length += 1
        return self

    # Time: O(1) | Space: O(1)
    def prepend(self, value: T) -> DoublyLinkedList[T]:
        new_node = Node(value, previous=None, next=self.head)

        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.head.previous = new_node
            self.head = new_node

        self._length += 1
        return self

    # Time: O(1) | Space: O(1)
    def remove_last(self) -> T:
        if self.head is None or self.tail is None:
            raise IndexError("List is empty.")

        former_tail = self.tail
        if self._length == 1:
            self.head = self.tail = None
        else:
            self.tail = former_tail.previous
            former_tail.previous = None
            assert self.tail is not None
            self.tail.next = None

        self._length -= 1
        return former_tail.value

    # Time: O(1) | Space: O(1)
    def remove_first(self) -> T:
        if self.head is None or self.tail is None:
            raise IndexError("List is empty.")

        former_head = self.head
        if self._length == 1:
            self.head = self.tail = None
        else:
            self.head = former_head.next
            assert self.head is not None
            self.head.previous = None
            former_head.next = None

        self._length -= 1
        return former_head.value

    # Time: O(n) | Space: O(1)
    def remove(self, value: T) -> T:
        if self.head is None or self.tail is None:
            raise IndexError("List is empty")

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
            return self.remove_last()

        current_node.next.previous = previous_node
        previous_node.next = current_node.next
        current_node.previous = current_node.next = None

        self._length -= 1
        return current_node.value
