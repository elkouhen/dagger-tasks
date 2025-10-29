import dagger
from dagger import dag, function, object_type


@object_type
class DaggerTasks:
    @function
    def container_echo(self, string_arg: str) -> dagger.Container:
        """Returns a container that echoes whatever string argument is provided"""
        return dag.container().from_("alpine:latest").with_exec(["echo", string_arg])

    @function
    async def build_mvn(self, source: dagger.Directory, image_name: str) -> str:
        """
        Builds a Maven project from the provided source directory and publishes the image to the specified image name.
        :param source: The source directory containing the Maven project.
        :param image_name: The name of the image to publish.
        :return: The reference of the published image.
        """
        return await (dag.container()
                      .from_("maven:latest")
                      .with_mounted_directory("/src", source)
                      .with_workdir("/src")
                      .with_exec(["mvn", "clean", "install", "-DskipTests"])
                      .with_entrypoint(["mvn", "spring-boot:run"])
                      .publish(image_name))
