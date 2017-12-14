from invoke import task


@task
def hello(ctx):
    "Say hello"
    print('Hello!')
