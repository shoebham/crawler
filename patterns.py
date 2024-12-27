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
            }

        }    
    def get_patterns(self,url):
        domain = urlparse(url).netloc.replace('www.', '')
        return self.url_patterns[domain]