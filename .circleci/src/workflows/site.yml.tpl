# Run jobs for the ${SITE} site
${SITE}:
  when: << pipeline.parameters.run_${SITE} >>
  jobs:
    # Check CHANGELOG update
    - check-changelog:
        name: check-changelog-${SITE}
        site: ${SITE}
        filters:
          branches:
            ignore: master
          tags:
            only: /.*/
    - lint-changelog:
        name: lint-changelog--${SITE}
        site: ${SITE}
        filters:
          branches:
            ignore: master
          tags:
            only: /.*/

    # Front-end jobs
    #
    # Build & lint the front-end apps
    - build-front-production:
        name: build-front-production-${SITE}
        site: ${SITE}
        filters:
          tags:
            only: /.*/
    - lint-front:
        name: lint-front-${SITE}
        site: ${SITE}
        requires:
          - build-front-production-${SITE}
        filters:
          tags:
            only: /.*/

    # Backend jobs
    #
    # Build, lint and test production and development Docker images
    # (debian-based)
    - build-back:
        name: build-back-${SITE}
        site: ${SITE}
        filters:
          tags:
            only: /.*/
    - lint-back:
        name: lint-back-${SITE}
        site: ${SITE}
        requires:
          - build-back-${SITE}
        filters:
          tags:
            only: /.*/
    - test-back:
        name: test-back-${SITE}
        site: ${SITE}
        requires:
          - build-back-${SITE}
        filters:
          tags:
            only: /.*/

    # DockerHub publication.
    #
    # Publish docker images only if all build, lint and test jobs succeed and
    # if the CI workflow has been triggered by a git tag starting with the
    # letter v or by a PR merged to the master branch
    - hub:
        name: hub-${SITE}
        site: ${SITE}
        requires:
          - lint-front-${SITE}
          - lint-back-${SITE}
        filters:
          tags:
            only: /^${SITE}-.*/
