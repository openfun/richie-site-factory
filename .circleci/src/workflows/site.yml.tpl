# Run jobs for the ${SITE} site
${SITE}:
  when: << pipeline.parameters.run_${SITE} >>
  jobs:
    # Check CHANGELOG update
    - check-changelog:
        site: ${SITE}
        filters:
          branches:
            ignore: master
          tags:
            only: /.*/
    - lint-changelog:
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
        site: ${SITE}
        filters:
          tags:
            only: /.*/
    - lint-front:
        site: ${SITE}
        requires:
          - build-front-production
        filters:
          tags:
            only: /.*/

    # Backend jobs
    #
    # Build, lint and test production and development Docker images
    # (debian-based)
    - build-back:
        site: ${SITE}
        filters:
          tags:
            only: /.*/
    - lint-back:
        site: ${SITE}
        requires:
          - build-back
        filters:
          tags:
            only: /.*/
    - test-back:
        site: ${SITE}
        requires:
          - build-back
        filters:
          tags:
            only: /.*/

    # DockerHub publication.
    #
    # Publish docker images only if all build, lint and test jobs succeed and
    # if the CI workflow has been triggered by a git tag starting with the
    # letter v or by a PR merged to the master branch
    - hub:
        site: ${SITE}
        requires:
          - lint-front
          - lint-back
        filters:
          tags:
            only: /^${SITE}-.*/
