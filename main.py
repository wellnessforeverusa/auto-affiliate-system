from sheet_service import get_next_product
from content_engine import generate_post
from dedupe import is_duplicate
from publisher import publish_blog
from outreach_engine import run_outreach
from utils.logging_utils import log

def main(request=None):
    log("Starting automation cycle...")
    
    product = get_next_product()
    if not product:
        log("No pending product found. Cycle complete.")
        return {"status": "no products"}

    log(f"Processing product: {product['name']}")

    content = generate_post(product)
    if is_duplicate(content, product["id"]):
        log("Duplicate detected, regenerating...")
        content = generate_post(product, force_new=True)

    post_url = publish_blog(content, product)
    run_outreach(product, post_url)

    log("Cycle finished.")
    return {"status": "success", "url": post_url}
