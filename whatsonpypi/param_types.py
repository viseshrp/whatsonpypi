import click


class MultipleChoice(click.Choice):
    """
    extension of click.Choice that
    accepts multiple choice inputs
    and converts them into a list
    """

    name = "Multiple Choice Param Type"

    def convert(self, value, param, ctx):
        cleaned_value = value.strip()

        if cleaned_value in self.choices:
            return [cleaned_value]

        choice_list = cleaned_value.split(",")
        valid_choice_list = []

        for choice in choice_list:
            choice = (
                choice.strip().lower()
            )  # lower is for when we have a,b,c as options.
            if choice not in self.choices:
                self.fail(
                    "Invalid choice: %s (choose from %s)"
                    % (choice, ", ".join(self.choices)),
                    param,
                    ctx,
                )

            valid_choice_list.append(choice)

        return valid_choice_list
