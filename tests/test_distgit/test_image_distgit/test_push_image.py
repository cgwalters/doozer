import errno
import os
import sys
import unittest

import flexmock

import distgit


class TestImageDistGitRepoPushImage(unittest.TestCase):

    def test_push_image_is_late_push(self):
        metadata = flexmock(config=flexmock(push=flexmock(late=True),
                                            distgit=flexmock(branch="_irrelevant_")),
                            distgit_key="distgit_key",
                            runtime=flexmock(branch="_irrelevant_"),
                            name="_irrelevant_",
                            logger=flexmock(info=lambda *_: None))

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)

        expected = ("distgit_key", True)
        actual = repo.push_image([], "push_to_defaults")
        self.assertEqual(expected, actual)

    def test_push_image_nothing_to_push(self):
        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            distgit=flexmock(branch="_irrelevant_")),
                            distgit_key="distgit_key",
                            get_default_push_names=lambda *_: [],
                            get_additional_push_names=lambda *_: [],
                            runtime=flexmock(branch="_irrelevant_"),
                            name="_irrelevant_",
                            logger=flexmock(info=lambda *_: None))

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        push_to_defaults = False

        expected = ("distgit_key", True)
        actual = repo.push_image([], push_to_defaults)
        self.assertEqual(expected, actual)

    def test_push_image_to_defaults(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os).should_receive("mkdir").replace_with(lambda _: None)
        flexmock(distgit.os.path).should_receive("isdir").and_return(True)
        flexmock(distgit.os.path).should_receive("isfile").and_return(True)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        # preventing tests from executing real commands
        flexmock(distgit.exectools).should_receive("cmd_gather").and_return((0, "", ""))

        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=False),
                                             working_dir="my-working-dir",
                                             branch="_irrelevant_",
                                             command="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            get_default_push_names=lambda *_: ["my-default-name"],
                            get_additional_push_names=lambda *_: [],
                            logger=flexmock(info=lambda *_: None),
                            namespace="_irrelevant_")

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = ["tag-a", "tag-b"]
        push_to_defaults = True

        expected = ("my-distgit-key", True)
        actual = repo.push_image(tag_list,
                                 push_to_defaults,
                                 version_release_tuple=("version", "release"))
        self.assertEqual(expected, actual)

    def test_push_image_without_version_release_tuple(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os).should_receive("mkdir").replace_with(lambda _: None)
        flexmock(distgit.os.path).should_receive("isdir").and_return(True)
        flexmock(distgit.os.path).should_receive("isfile").and_return(True)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        # preventing tests from executing real commands
        flexmock(distgit.exectools).should_receive("cmd_gather").and_return((0, "", ""))

        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=False),
                                             working_dir="my-working-dir",
                                             branch="_irrelevant_",
                                             command="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            get_latest_build_info=lambda *_: ("_", "my-version", "my-release"),
                            get_default_push_names=lambda *_: ["my-default-name"],
                            get_additional_push_names=lambda *_: [],
                            logger=flexmock(info=lambda *_: None),
                            namespace="_irrelevant_")

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = ["tag-a", "tag-b"]
        push_to_defaults = True

        expected = ("my-distgit-key", True)
        actual = repo.push_image(tag_list, push_to_defaults)
        self.assertEqual(expected, actual)

    def test_push_image_no_push_tags(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os).should_receive("mkdir").replace_with(lambda _: None)
        flexmock(distgit.os.path).should_receive("isdir").and_return(True)
        flexmock(distgit.os.path).should_receive("isfile").and_return(True)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        # preventing tests from executing real commands
        flexmock(distgit.exectools).should_receive("cmd_gather").and_return((0, "", ""))

        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=False),
                                             working_dir="my-working-dir",
                                             branch="_irrelevant_",
                                             command="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            namespace="my-namespace",
                            get_latest_build_info=lambda *_: ("_", "my-version", "my-release"),
                            get_default_push_names=lambda *_: ["my/default-name"],
                            get_default_push_tags=lambda *_: [],
                            get_additional_push_names=lambda *_: [],
                            logger=flexmock(info=lambda *_: None))

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = []
        push_to_defaults = True

        expected = ("my-distgit-key", True)
        actual = repo.push_image(tag_list,
                                 push_to_defaults,
                                 version_release_tuple=("version", "release"),
                                 dry_run=True)
        self.assertEqual(expected, actual)

    def test_push_image_dry_run(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os).should_receive("mkdir").replace_with(lambda _: None)
        flexmock(distgit.os.path).should_receive("isdir").and_return(True)
        flexmock(distgit.os.path).should_receive("isfile").and_return(True)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        # preventing tests from executing real commands
        flexmock(distgit.exectools).should_receive("cmd_gather").and_return((0, "", ""))

        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=False),
                                             working_dir="my-working-dir",
                                             branch="_irrelevant_",
                                             command="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            namespace="my-namespace",
                            get_default_push_names=lambda *_: ["my-default-name"],
                            get_additional_push_names=lambda *_: [],
                            logger=flexmock(info=lambda *_: None))

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = ["tag-a", "tag-b"]
        push_to_defaults = True

        expected = ("my-distgit-key", True)
        actual = repo.push_image(tag_list,
                                 push_to_defaults,
                                 version_release_tuple=("version", "release"),
                                 dry_run=True)
        self.assertEqual(expected, actual)

    def test_push_image_without_a_push_config_dir_previously_present(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os).should_receive("mkdir").replace_with(lambda _: None)
        flexmock(distgit.os.path).should_receive("isdir").and_return(False)
        flexmock(distgit.os.path).should_receive("isfile").and_return(True)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        # preventing tests from executing real commands
        flexmock(distgit.exectools).should_receive("cmd_gather").and_return((0, "", ""))

        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=False),
                                             working_dir="my-working-dir",
                                             branch="_irrelevant_",
                                             command="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            namespace="my-namespace",
                            get_default_push_names=lambda *_: ["my-default-name"],
                            get_additional_push_names=lambda *_: [],
                            logger=flexmock(info=lambda *_: None))

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = ["tag-a", "tag-b"]
        push_to_defaults = True

        expected = ("my-distgit-key", True)
        actual = repo.push_image(tag_list,
                                 push_to_defaults,
                                 version_release_tuple=("version", "release"))
        self.assertEqual(expected, actual)

    def test_push_image_fail_to_create_a_push_config_dir(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os.path).should_receive("isdir").and_return(False)
        flexmock(distgit.os.path).should_receive("isfile").and_return(True)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        # simulating an error on mkdir attempt
        flexmock(distgit.os).should_receive("mkdir").and_raise(OSError)

        # preventing tests from executing real commands
        flexmock(distgit.exectools).should_receive("cmd_gather").and_return((0, "", ""))

        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=False),
                                             working_dir="my-working-dir",
                                             branch="_irrelevant_",
                                             command="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            namespace="my-namespace",
                            get_default_push_names=lambda *_: ["my-default-name"],
                            get_additional_push_names=lambda *_: [],
                            logger=flexmock(info=lambda *_: None))

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = ["tag-a", "tag-b"]
        push_to_defaults = True
        version_release_tuple = ("version", "release")

        self.assertRaises(OSError,
                          repo.push_image,
                          tag_list,
                          push_to_defaults,
                          version_release_tuple=version_release_tuple)

    def test_push_image_push_config_dir_already_created_by_another_thread(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os.path).should_receive("isdir").and_return(False).and_return(True)
        flexmock(distgit.os.path).should_receive("isfile").and_return(False)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        # simulating an "already exists" error on mkdir attempt
        (flexmock(distgit.os)
            .should_receive("mkdir")
            .and_raise(OSError(errno.EEXIST, os.strerror(errno.EEXIST))))

        # preventing tests from executing real commands
        flexmock(distgit.exectools).should_receive("cmd_gather").and_return((0, "", ""))

        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=False),
                                             working_dir="my-working-dir",
                                             branch="_irrelevant_",
                                             command="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            namespace="my-namespace",
                            get_default_push_names=lambda *_: ["my-default-name"],
                            get_additional_push_names=lambda *_: [],
                            logger=flexmock(info=lambda *_: None))

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = ["tag-a", "tag-b"]
        push_to_defaults = True

        expected = ("my-distgit-key", True)
        actual = repo.push_image(tag_list,
                                 push_to_defaults,
                                 version_release_tuple=("version", "release"))
        self.assertEqual(expected, actual)

    def test_push_image_to_defaults_fail_mirroring(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os).should_receive("mkdir").replace_with(lambda _: None)
        flexmock(distgit.os.path).should_receive("isdir").and_return(True)
        flexmock(distgit.os.path).should_receive("isfile").and_return(True)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        # simulating an error while executing cmd_gather
        (flexmock(distgit.exectools)
            .should_receive("cmd_gather")
            .and_return((1, "", "stderr")))

        # a failed cmd_gather will try again in X seconds, we don't want to wait
        flexmock(distgit.time).should_receive("sleep").replace_with(lambda *_: None)

        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=False),
                                             working_dir="my-working-dir",
                                             branch="_irrelevant_",
                                             command="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            namespace="my-namespace",
                            get_default_push_names=lambda *_: ["my-default-name"],
                            get_additional_push_names=lambda *_: [],
                            logger=flexmock(info=lambda *_: None))

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = ["tag-a", "tag-b"]
        push_to_defaults = True
        version_release_tuple = ("version", "release")

        try:
            repo.push_image(tag_list,
                            push_to_defaults,
                            version_release_tuple=version_release_tuple)
            self.fail("Should have raised an exception, but didn't")
        except IOError as e:
            expected_msg = "Error pushing image: stderr"
            self.assertEqual(expected_msg, e.message)

    def test_push_image_to_defaults_with_lstate(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os).should_receive("mkdir").replace_with(lambda _: None)
        flexmock(distgit.os.path).should_receive("isdir").and_return(True)
        flexmock(distgit.os.path).should_receive("isfile").and_return(True)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        # preventing tests from executing real commands
        flexmock(distgit.exectools).should_receive("cmd_gather").and_return((0, "", ""))

        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=False),
                                             working_dir="my-working-dir",
                                             state={"images:push": "my-runtime-state"},
                                             command="images:push",
                                             branch="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            get_default_push_names=lambda *_: ["my-default-name"],
                            get_additional_push_names=lambda *_: [],
                            logger=flexmock(info=lambda *_: None),
                            namespace="_irrelevant_")

        (flexmock(distgit.state)
            .should_receive("record_image_success")
            .with_args("my-runtime-state", metadata)
            .once()
            .and_return(None))

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = ["tag-a", "tag-b"]
        push_to_defaults = True

        expected = ("my-distgit-key", True)
        actual = repo.push_image(tag_list,
                                 push_to_defaults,
                                 version_release_tuple=("version", "release"))
        self.assertEqual(expected, actual)

    def test_push_image_to_defaults_fail_mirroring_with_lstate(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os).should_receive("mkdir").replace_with(lambda _: None)
        flexmock(distgit.os.path).should_receive("isdir").and_return(True)
        flexmock(distgit.os.path).should_receive("isfile").and_return(True)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        # simulating an error while executing cmd_gather
        (flexmock(distgit.exectools)
            .should_receive("cmd_gather")
            .and_return((1, "", "stderr")))

        # a failed cmd_gather will try again in X seconds, we don't want to wait
        flexmock(distgit.time).should_receive("sleep").replace_with(lambda *_: None)

        logger = flexmock(info=lambda *_: None)
        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=False),
                                             working_dir="my-working-dir",
                                             state={"images:push": "my-runtime-state"},
                                             command="images:push",
                                             logger=logger,
                                             branch="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            namespace="my-namespace",
                            get_default_push_names=lambda *_: ["my-default-name"],
                            get_additional_push_names=lambda *_: [],
                            logger=logger)

        (flexmock(distgit.state)
            .should_receive("record_image_fail")
            .with_args("my-runtime-state", metadata, "Build failure", logger)
            .once()
            .ordered()
            .and_return(None))

        expected_msg = "Error pushing image: stderr"

        (flexmock(distgit.state)
            .should_receive("record_image_fail")
            .with_args("my-runtime-state", metadata, expected_msg, logger)
            .once()
            .ordered()
            .and_return(None))

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = ["tag-a", "tag-b"]
        push_to_defaults = True
        version_release_tuple = ("version", "release")

        try:
            repo.push_image(tag_list,
                            push_to_defaults,
                            version_release_tuple=version_release_tuple)
            self.fail("Should have raised an exception, but didn't")
        except IOError as e:
            self.assertEqual(expected_msg, e.message)

    def test_push_image_insecure_source(self):
        # preventing tests from interacting with the real filesystem
        flexmock(distgit).should_receive("Dir").and_return(flexmock(__exit__=None))
        flexmock(distgit.os).should_receive("mkdir").replace_with(lambda _: None)
        flexmock(distgit.os.path).should_receive("isdir").and_return(True)
        flexmock(distgit.os.path).should_receive("isfile").and_return(True)
        flexmock(distgit.os).should_receive("remove").replace_with(lambda _: None)
        (flexmock(sys.modules["__builtin__"])
            .should_receive("open")
            .and_return(flexmock(write=lambda *_: None,
                                 readlines=lambda *_: [])))

        expected_cmd = "oc image mirror  --insecure=true --filename=my-working-dir/push/my-distgit-key"

        (flexmock(distgit.exectools)
            .should_receive("cmd_gather")
            .with_args(expected_cmd)
            .once()
            .and_return((0, "", "")))

        metadata = flexmock(config=flexmock(push=flexmock(late=distgit.Missing),
                                            name="my-name",
                                            namespace="my-namespace",
                                            distgit=flexmock(branch="_irrelevant_")),
                            runtime=flexmock(group_config=flexmock(urls=flexmock(brew_image_host="brew-img-host"),
                                                                   insecure_source=True),
                                             working_dir="my-working-dir",
                                             branch="_irrelevant_",
                                             command="_irrelevant_",
                                             add_record=lambda *_, **__: None),
                            distgit_key="my-distgit-key",
                            name="my-name",
                            get_default_push_names=lambda *_: ["my-default-name"],
                            get_additional_push_names=lambda *_: [],
                            logger=flexmock(info=lambda *_: None),
                            namespace="_irrelevant_")

        repo = distgit.ImageDistGitRepo(metadata, autoclone=False)
        tag_list = ["tag-a", "tag-b"]
        push_to_defaults = True

        expected = ("my-distgit-key", True)
        actual = repo.push_image(tag_list,
                                 push_to_defaults,
                                 version_release_tuple=("version", "release"))
        self.assertEqual(expected, actual)