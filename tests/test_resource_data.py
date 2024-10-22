import unittest
from unittest.mock import patch, Mock
from resource_data import ResourceEprint

class TestResourceDataFetcher(unittest.TestCase):
    
    def test_fetch_and_process_data_success(self):
        # Mock a successful response
        res = ResourceEprint([
            "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2024/JSON/if_2024.js",
            "https://eprints.amikom.ac.id/cgi/exportview/divisions/if/2023/JSON/if_2023.js"
        ])

        res = res.process()
        print(f"res {res}")
        pass

if __name__ == '__main__':
    unittest.main()