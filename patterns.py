from urllib.parse import urljoin, urlparse


class Patterns:

    def __init__(self):
        self.generic_product_patterns = {
            r"\/p\/\d+",           # Common pattern: /p/123456
            r"\/product\/[\w-]+",  # Common pattern: /product/product-name
            r"\/item\/[\w-]+",     # Common pattern: /item/item-name
            r"\/[\w-]+\/p\/[\w-]+", # Common pattern: /category/p/product-name
            r"\/products\/[\w-]+", # Common pattern: /products/product-name
            r"\/[\w-]+-p\d+",     # Common pattern: /product-name-p123456
            r"\/buy\/[\w-]+",      # Common pattern: /buy/product-name
            r"\/dp\/[\w\d]+",      # Common pattern like Amazon: /dp/B12345
            r"\/\d+\/buy$"         # Pattern ending with buy
        } 
            
        self.generic_exclude_patterns = {
            r"\/cart",
            r"\/wishlist",
            r"\/login",
            r"\/signup",
            r"\/account",
            r"\/profile",
            r"\/checkout",
            r"\/search",
            r"\/category",
            r"\/shop\/",
            r"\/stores?\/",
            r"\/brands?\/",
            r"\/support",
            r"\/contact",
            r"\/help",
            r"\/about",
            r"\/auth",
            r"\/register",
            r"\/password",
            r"\/order"
        }

    def get_patterns(self, url):
        return {
            "product_patterns": self.generic_product_patterns,
            "exclude_patterns": self.generic_exclude_patterns
        }