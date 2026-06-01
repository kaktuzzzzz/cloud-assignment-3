import random
from locust import HttpUser, task, constant

class NguyenPandaCrazyTest(HttpUser):

    wait_time = constant(0)

    @task(100)
    def hammer_index(self):
        self.client.get("/", name="01_HAMMER_INDEX")

    @task(50)
    def crawl_all_pages(self):
        pages = [
            "/research", "/projects", "/hpc", "/gallery", 
            "/archive", "/portal", "/about",
        ]
        self.client.get(random.choice(pages), name="02_CRAWL_PAGES")

    @task(40)
    def static_asset_burst(self):
        assets = [
            "/public/styles/style.css",
            "/public/scripts/script.js",
            "/public/images/meme/Dogo.gif",
            "/public/images/nguyenpanda/png/logo_black_bg.png",
            "/public/data/site.yaml",
            "/public/data/navigation.yaml"
        ]
        self.client.get(random.choice(assets), name="03_STATIC_BOMB")

    @task(20)
    def redirect_stress(self):
        self.client.get("/home", name="04_REDIRECT_STRESS")

    @task(10)
    def chaos_404_bomb(self):
        """Randomized paths to force 404 handler execution"""
        junk_path = f"/chaos/attack_{random.randint(1, 1000000)}"
        self.client.get(junk_path, name="05_CHAOS_404")
