from datacontract.model.data_contract_specification import DataContractSpecification

from ..lint import Linter, LinterResult


class FieldReferenceLinter(Linter):
    """Checks that all references definitions in fields refer to existing
    fields.

    """

    @property
    def name(self):
        return "Field references existing field"

    @property
    def id(self) -> str:
        return "field-reference"

    def lint_implementation(self, contract: DataContractSpecification) -> LinterResult:
        result = LinterResult()
        for model_name, model in contract.models.items():
            for field_name, field in model.fields.items():
                if field.references:
                    reference_hierarchy = field.references.split(".")
                    if len(reference_hierarchy) != 2:
                        result = result.with_error(
                            f"Field '{field_name}' in model '{model_name}'"
                            f" references must follow the model.field syntax and refer to a field in a model in this data contract."
                        )
                        continue
                    ref_model = reference_hierarchy[0]
                    ref_field = reference_hierarchy[1]

                    if ref_model not in contract.models:
                        result = result.with_error(
                            f"Field '{field_name}' in model '{model_name}' references non-existing model '{ref_model}'."
                        )
                    else:
                        ref_model_obj = contract.models[ref_model]
                        if ref_field not in ref_model_obj.fields:
                            result = result.with_error(
                                f"Field '{field_name}' in model '{model_name}'"
                                f" references non-existing field '{ref_field}'"
                                f" in model '{ref_model}'."
                            )
        return result
