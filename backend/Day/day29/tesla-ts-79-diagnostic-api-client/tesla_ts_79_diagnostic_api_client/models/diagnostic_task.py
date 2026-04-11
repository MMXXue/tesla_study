from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DiagnosticTask")


@_attrs_define
class DiagnosticTask:
    """
    Attributes:
        vin (str): 车辆17位唯一识别码 Example: 5YJ3E1EB....
        fault_code (str): 传感器捕获的故障码 Example: BMS_a066.
    """

    vin: str
    fault_code: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vin = self.vin

        fault_code = self.fault_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vin": vin,
                "fault_code": fault_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vin = d.pop("vin")

        fault_code = d.pop("fault_code")

        diagnostic_task = cls(
            vin=vin,
            fault_code=fault_code,
        )

        diagnostic_task.additional_properties = d
        return diagnostic_task

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
