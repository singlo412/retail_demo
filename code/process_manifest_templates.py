import os
import logging
import glob
from jinja2 import Environment, FileSystemLoader

# Configure logging with basic settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_templates():
    """
    Process the manifest templates based on the S3 asset bucket

    Args:
        creds (dict, optional): AWS credentials dictionary. If None, 
        it uses the default credentials.

    Returns:
        None
    """
    s3_bucket = os.environ.get("QBIZ_ASSET_BUCKET_NAME", None)
    if s3_bucket is None:
        logger.error("Required QBIZ_ASSET_BUCKET_NAME environment variable is not set")
        exit(1)

    buckets = {
        "qbiz_asset": s3_bucket
    }

    tpl_environment = Environment(loader=FileSystemLoader("manifest_templates/"), autoescape=True)
    tpl_fnames = glob.glob("manifest_templates/*.j2")
    for tmp_fname in tpl_fnames:
        tpl_fname = tmp_fname.split("/")[-1]
        out_fname = "manifest/"+tpl_fname[:-3]
        logger.info(f"Processing: {tpl_fname}")
        template = tpl_environment.get_template(tpl_fname)
        content = template.render(buckets=buckets)
        with open(out_fname, mode="w", encoding="utf-8") as message:
            message.write(content)
            logger.info(f"  Saved: {out_fname}")

process_templates()
exit(0)
