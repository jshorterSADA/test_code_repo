import asyncio
import logging
import os
import sys
import unittest
from unittest.mock import patch, MagicMock, AsyncMock

# Original import statement
# We rename it to 'original_agent_main' to avoid name conflicts when mocking 'main'
# and to make it clear we are referring to the actual function from .agent.
from .agent import main as original_agent_main

# Configure logging for the main script
# The logger is defined at the module level so it can be easily patched for tests.
logger = logging.getLogger(__name__)


def _run_agent_process():
    """
    Configures environment variables and runs the agent's main function.
    This function encapsulates the logic from the original __main__ block,
    making it testable.
    """
    try:
        # Define expected integer environment variables and their default values
        int_env_vars = {
            'AGENT_PORT': 8080,
            'AGENT_TIMEOUT': 300,
        }

        for var_name, default_int_value in int_env_vars.items():
            current_value = os.getenv(var_name)
            
            # Try to convert the current value to an integer
            try:
                if current_value is not None:
                    parsed_value = int(current_value)
                    # If successful, ensure it's set as a string in os.environ
                    os.environ[var_name] = str(parsed_value)
                else:
                    # If the variable is not set, use the default integer value
                    os.environ[var_name] = str(default_int_value)
            except ValueError:
                # If current_value is not convertible to int (e.g., "abc")
                logger.warning(
                    f"Environment variable '{var_name}' has an invalid integer value "
                    f"'{current_value}'. Using default value '{default_int_value}'."
                )
                os.environ[var_name] = str(default_int_value)

        asyncio.run(original_agent_main())
    except KeyboardInterrupt:
        logger.info("Agent execution stopped by user.")


if __name__ == "__main__":
    # Check if the script is run with 'test' as an argument.
    # This allows running tests by: python your_script.py test
    # And normal execution by: python your_script.py
    if "test" in sys.argv:
        # Remove 'test' from sys.argv so unittest.main doesn't try to interpret it
        # as a test name or module, which would cause an error.
        sys.argv.remove("test")
        # Run tests. unittest.main() will discover tests in the current module.
        # exit=False prevents unittest.main from calling sys.exit(), allowing
        # the script to potentially continue or for a cleaner exit in some environments.
        unittest.main(module=__name__, exit=False)
    else:
        # Normal execution path: run the agent process.
        _run_agent_process()