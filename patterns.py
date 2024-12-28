from urllib.parse import urljoin, urlparse


class Patterns:

    def __init__(self):
        self.url_patterns = {
            "myntra.com":
            {
                "product_patterns":
                {
                    r"/\d+/buy$"
                },
                "exclude_patterns":
                {
                    r"/shop/",
                    r"/wishlist",
                    r"/cart",
                    r"/login",
                    r"/profile",
                    r"/checkout",
                    r"/account",
                    r"/search"
                }
            },
            "ajio.com":{ 
                "product_patterns":
                {
                    r"/[^/]+/p/\d+[^/]*$"
                    
                },
                "exclude_patterns":
                {
                    r"/shop/",
                    r"/wishlist",
                    r"/cart",
                    r"/login",
                    r"/profile",
                    r"/checkout",
                    r"/account",
                    r"/search"
                }
            } 

        }  
    def get_patterns(self,url):
        domain = urlparse(url).netloc.replace('www.', '')
        default_pattern = {
            "product_patterns": [
                r"/product/",
                r"/p/",
                r"/item/",
                r"/buy"
            ],
            "exclude_patterns": [
                r"/cart",
                r"/wishlist",
                r"/login",
                r"/account"
            ]
        }
        return self.url_patterns.get(domain,default_pattern)