import schedule
import time
import logging
import scraper

logging.basicConfig(filename="scheduler.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def job():
    logging.info("Launching scraping...")
    scraper.main()
    logging.info("Scraping done.")

# Execute the job every hour
schedule.every().minute.do(job)

if __name__ == "__main__":
    logging.info("Initialize scheduler.")
    while True:
        schedule.run_pending()
        time.sleep(1)
