from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    @task(1)
    def search_page(self):
        self.client.get("/markets")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
