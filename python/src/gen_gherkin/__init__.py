"""__init__.py module for the Generate Gherkin Feature Files plugin."""

# WARNING - DO NOT EDIT - YOUR CHANGES WILL NOT BE PROTECTED.
# This file is auto-generated by the aac gen-plugin and may be overwritten.

from os.path import join, dirname

from aac.context.language_context import LanguageContext
from aac.execute import hookimpl
from aac.execute.aac_execution_result import ExecutionResult, ExecutionStatus
from aac.execute.plugin_runner import PluginRunner

from aac.plugins.check import run_check
from aac.plugins.generate import run_generate

from gen_gherkin.generate_gherkin_feature_files_impl import (
    plugin_name,
    before_gen_gherkin_behaviors,
    gen_gherkin_behaviors,
    after_gen_gherkin_behaviors,
)


generate_gherkin_feature_files_aac_file_name = "generate_gherkin_feature_files.aac"


def run_gen_gherkin_behaviors(
    architecture_file: str, output_directory: str
) -> ExecutionResult:
    """
    Generate Gherkin feature files from AaC model behavior scenarios.

    Args:
        architecture_file (str): The YAML file containing the data models from which to generate Gherkin feature files.
        output_directory (str): The directory into which the generated Gherkin feature files will be written.

    Returns:
        The results of the execution of the plugin gen-gherkin-behaviors command.
    """

    result = ExecutionResult(
        plugin_name, "gen-gherkin-behaviors", ExecutionStatus.SUCCESS, []
    )

    gen_gherkin_check_result = before_gen_gherkin_behaviors(architecture_file, run_check)
    if not gen_gherkin_check_result.is_success():
        return gen_gherkin_check_result
    else:
        result.add_messages(gen_gherkin_check_result.messages)

    content, gen_gherkin_behaviors_result = gen_gherkin_behaviors(
        architecture_file, output_directory
    )
    if not gen_gherkin_behaviors_result.is_success():
        return gen_gherkin_behaviors_result
    else:
        result.add_messages(gen_gherkin_behaviors_result.messages)

    gen_gherkin_behaviors_generate_result = after_gen_gherkin_behaviors(
        architecture_file, output_directory, run_generate
    )
    if not gen_gherkin_behaviors_generate_result.is_success():
        return gen_gherkin_behaviors_generate_result
    else:
        result.add_messages(gen_gherkin_behaviors_generate_result.messages)

    return result


@hookimpl
def register_plugin() -> None:
    """
    Registers information about the plugin for use in the CLI.

    Returns:
        A collection of information about the plugin and what it contributes.
    """

    active_context = LanguageContext()
    generate_gherkin_feature_files_aac_file = join(
        dirname(__file__), generate_gherkin_feature_files_aac_file_name
    )
    definitions = active_context.parse_and_load(generate_gherkin_feature_files_aac_file)

    generate_gherkin_feature_files_plugin_definition = [
        definition for definition in definitions if definition.name == plugin_name
    ][0]

    plugin_instance = generate_gherkin_feature_files_plugin_definition.instance
    for file_to_load in plugin_instance.definition_sources:
        active_context.parse_and_load(file_to_load)

    plugin_runner = PluginRunner(
        plugin_definition=generate_gherkin_feature_files_plugin_definition
    )
    plugin_runner.add_command_callback(
        "gen-gherkin-behaviors", run_gen_gherkin_behaviors
    )

    active_context.register_plugin_runner(plugin_runner)
