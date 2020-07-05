import traceback
import logging

from api_app.exceptions import AnalyzerRunException
from api_app.script_analyzers import general
from intel_owl import secrets

logger = logging.getLogger(__name__)


def run(
    analyzer_name,
    job_id,
    observable_name,
    observable_classification,
    additional_config_params,
):
    logger.info(
        f"started analyzer {analyzer_name} job_id {job_id} observable {observable_name}"
    )
    report = general.get_basic_report_template(analyzer_name)
    try:
        api_key_name = additional_config_params.get("api_key_name", "KEY_NAME")
        api_key = secrets.get_secret(api_key_name)
        if not api_key:
            raise AnalyzerRunException("no api key retrieved")

        result = {}
        # do something here

        # pprint.pprint(result)
        report["report"] = result
    except AnalyzerRunException as e:
        error_message = (
            f"job_id:{job_id} analyzer:{analyzer_name}"
            f" observable_name:{observable_name} Analyzer error {e}"
        )
        logger.error(error_message)
        report["errors"].append(error_message)
        report["success"] = False
    except Exception as e:
        traceback.print_exc()
        error_message = (
            f"job_id:{job_id} analyzer:{analyzer_name}"
            f" observable_name:{observable_name} Unexpected error {e}"
        )
        logger.exception(error_message)
        report["errors"].append(str(e))
        report["success"] = False
    else:
        report["success"] = True

    general.set_report_and_cleanup(job_id, report)

    logger.info(
        "ended analyzer {analyzer_name} job_id {job_id} observable {observable_name}"
    )

    return report