from __future__ import annotations

from typing import Any

import click


class MultipleChoice(click.Choice):
    """
    extension of click.Choice that
    accepts multiple choice inputs
    and converts them into a list
    """

    name: str = "Multiple Choice Param Type"

    def convert(
        self, value: Any, param: click.Parameter | None, ctx: click.Context | None
    ) -> list[str]:
        cleaned_value = value.strip()

        if cleaned_value in self.choices:
            return [cleaned_value]

        choice_list = cleaned_value.split(",")
        valid_choice_list = []

        for choice in choice_list:
            choice = choice.strip().lower()  # lower is for when we have a,b,c as options.
            if choice not in self.choices:
                self.fail(
                    "Invalid choice: {} (choose from {})".format(choice, ", ".join(self.choices)),
                    param,
                    ctx,
                )

            valid_choice_list.append(choice)

        return valid_choice_list
