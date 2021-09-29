(function () {
  /**
   * Deserialize a context analytic dimension
   *
   * @param dimension - string with items joined by ' | '
   * @return data
   *    - undefined if the dimension string was empty
   *    - A single value if the dimension cannot be split
   *    - An array of value if dimension has been split
   */
  function deserialize(dimension) {
    const data = dimension.split(' | ');
    if (data.length === 1) {
      if (!data[0].trim()) return undefined;
      return data[0];
    }
    return data;
  }

  /**
   *
   * An object to initialize then use AT Internet SmartTag.
   *
   * @param metadata - analytics context
   *
   *  - id: AT Internet site id to identify the site on Analytics Suite
   *  - provider: 'xiti',
   *  - dimensions: some serialized data related to the current page
   *    + course_code
   *    + course_runs_resource_links
   *    + course_runs_titles
   *    + organizations_codes
   *    + page_title
   *    + root_page_id: level2
   *
   */
  function SmartTag(metadata) {
    this.data = null;
    this.level2 = metadata.dimensions.root_page_id;
    this.organizations = deserialize(metadata.dimensions.organizations_codes);
    this.siteId = metadata.id;
    this.tag = null;

    /**
     * Populate the data object sent to Xiti on dispatch.
     * It includes level2, name and chapters
     *
     * To get name and chapters we split the url pathname "/"
     * name is the first element of this destructuring
     * chapters are the remaining elements
     */
    this.populateData = function () {
      var self = this;
      var chapters = location.pathname
        .split('/')
        .filter(function (slug) {
          return slug.length > 0;
        })
        .slice(1); // Remove lang

      var name = chapters.shift();

      this.data = {
        level2: this.level2,
        name: name || '/',
      };

      chapters.forEach(function (chapter, index) {
        self.data['chapter' + (index + 1)] = '[' + chapter + ']';
      });
    };

    /**
     * Dispatch data on page load
     * Set customVars, customObject and internalSearch if it is relevant
     * then dispatch a record.
     */
    this.dispatch = function () {
      // Detail language
      var lang = (document.documentElement.lang || '-').split('-')[0].toLowerCase();
      if (lang) {
        this.tag.customVars.set({ site: { 1: '[' + lang + ']' } });
      }

      // Detail organizations related to the page
      if (this.organizations && this.organizations.length > 0) {
        var serializedOrganizations =
          '[' +
          this.organizations
            .map(function (organization) {
              return '"' + organization + '"';
            })
            .toString() +
          ']';
        this.tag.setProp('a:s:organizations', serializedOrganizations, true);
      }

      // Detail search query if there is
      var search_query = new URL(location.href).searchParams.get('query');
      if (search_query) {
        this.tag.internalSearch.set({
          keyword: search_query,
        });
      }

      // Dispatch data
      this.tag.page.set(this.data);
      this.tag.dispatch();
    };

    /**
     * Instantiate the Xiti tag
     * Check if ATInternet exists then create a new tag.
     */
    this.createTag = function () {
      if (ATInternet) {
        this.tag = new ATInternet.Tracker.Tag({ site: this.siteId, secure: true });
      }
    };

    /**
     * Add click event listeners on all buttons on the page.
     * Send a record each time a visitor click on an action button on the page.
     */
    this.spyClickOnButtons = function () {
      var self = this;

      function spyClick(event) {
        var $target = event.currentTarget;
        var name = $target.innerText || $target.classList.value.replace(' ', '.');

        var parameters = self.data;
        parameters.elem = $target;
        parameters.name = name;
        parameters.type = 'action';

        self.tag.click.send(parameters);
      }

      // Some browsers do not implement `HTMLCollection.forEach` method
      // so we transform HTMLCollection into an Array
      var $buttons = [].slice.call(document.getElementsByTagName('button'));
      $buttons.forEach(($button) => {
        $button.addEventListener('click', spyClick, false);
      });
    };

    /**
     * Initialize SmartTag
     *
     * Create smartTag, populate data then dispatch a record
     * and add click listeners on buttons
     */
    this.init = function () {
      this.createTag();
      this.populateData();
      this.dispatch();
      this.spyClickOnButtons();
    };
  }

  var context = window.__funmooc_context__.analytics;
  tarteaucitron.services.xitiFun = {
    key: 'xiti',
    type: 'analytic',
    name: 'Xiti',
    uri: 'https://www.atinternet.com/societe/rgpd-et-vie-privee/',
    needConsent: false,
    cookies: ['atid', 'idrxvr', 'atuserid', 'atidx', 'atidvisitor'],
    js: function () {
      var smarttag_url = 'https://tag.aticdn.net/' + context.id + '/smarttag.js';
      function onLoad() {
        var smartTag = new SmartTag(context);
        smartTag.init();
      }
      tarteaucitron.addScript(smarttag_url, '', onLoad);
    },
  };
  tarteaucitron.job.push('xitiFun');
})();
