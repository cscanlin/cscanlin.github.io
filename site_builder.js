"use strict";

var Nightmare = require('nightmare');
var nightmare = Nightmare({ show: true });

const REPO_API_PATH = 'https://api.github.com/repos'

class Repository {

  constructor(repo_url, screenshot_target) {
    this.screenshot_target = screenshot_target ? screenshot_target : repo_data.homepage
    const repo_data = this.parse_data_from_url(repo_url)
    Object.keys(repo_data).forEach(key => {
      this[key] = repo_data[key]
    })
  }

  parse_data_from_url(repo_url) {
    const repo_data = {
      name: repo_url.split('/').reverse()[0],
      html_url: repo_url,
    }
    console.log(repo_data);
    repo_data.homepage = 'https://cscanlin.github.io/' + repo_data.name
    return repo_data
  }

  toString() {
    return this.name
  }
}

console.log(new Repository('https://github.com/cscanlin/munger-builder', 'target').toString());

// nightmare
//   .goto('https://duckduckgo.com')
//   .screenshot('test.png')
//   .goto('https://google.com')
//   .screenshot('test2.png')
//   .end()
//   .then(function (result) {
//     console.log(result);
//   })
