console.log('started')
const page = require('webpage').create()

page.viewportSize = {
  width: 1024,
  height: 768,
}

const REPOSITORY_URLS = [
  'https://github.com/cscanlin/munger-builder',
  'https://github.com/cscanlin/choice-optimizer',
  'https://github.com/cscanlin/minesweeper',
  'https://github.com/cscanlin/periodic-table-timeline',
]

function getRepoData(repoURL, callback) {
  const xhr = new XMLHttpRequest()
  xhr.open('GET', 'https://api.github.com/repos/cscanlin/munger-builder', true)
  xhr.responseType = 'json'
  xhr.onload = function () {
    console.log(xhr.response)
    // callback(JSON.parse(xhr.response))
  }
  xhr.send()
// https://api.github.com/repos/cscanlin/munger-builder
}

function generateScreenshot(repoData) {
  page.open(repoData.homepage, function () {
    page.render('screenshots/' + repoData.name + '.png')
    console.log('finished: ' + repoData.name)
    setTimeout(nextPage, 100)
  })
}

function nextPage() {
  const repoURL = REPOSITORY_URLS.shift()
  if (!repoURL) { phantom.exit(0) }
  getRepoData(repoURL, generateScreenshot)
}

nextPage()
