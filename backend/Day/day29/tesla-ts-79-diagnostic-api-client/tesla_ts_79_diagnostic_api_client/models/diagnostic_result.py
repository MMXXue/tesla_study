from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DiagnosticResult")


@_attrs_define
class DiagnosticResult:
    """
    Attributes:
        is_critical (bool): 是否属于致命故障
        suggestion (str): AI 给出的维修建议
    """

    is_critical: bool
    suggestion: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_critical = self.is_critical

        suggestion = self.suggestion

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_critical": is_critical,
                "suggestion": suggestion,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_critical = d.pop("is_critical")

        suggestion = d.pop("suggestion")

        diagnostic_result = cls(
            is_critical=is_critical,
            suggestion=suggestion,
        )

        diagnostic_result.additional_properties = d
        return diagnostic_result

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
