import comp from "D:/So_Iam_Os/project_docs/docs/.vuepress/.temp/pages/Learn_Vue/index.html.vue"
const data = JSON.parse("{\"path\":\"/Learn_Vue/\",\"title\":\"Learn Vue\",\"lang\":\"en-US\",\"frontmatter\":{},\"headers\":[{\"level\":2,\"title\":\"Create Project\",\"slug\":\"create-project\",\"link\":\"#create-project\",\"children\":[{\"level\":3,\"title\":\"Vue Libraries\",\"slug\":\"vue-libraries\",\"link\":\"#vue-libraries\",\"children\":[]}]},{\"level\":2,\"title\":\"🚀 Run Vue Project\",\"slug\":\"🚀-run-vue-project\",\"link\":\"#🚀-run-vue-project\",\"children\":[]},{\"level\":2,\"title\":\"📋 Vue Django\",\"slug\":\"📋-vue-django\",\"link\":\"#📋-vue-django\",\"children\":[]}],\"git\":{},\"filePathRelative\":\"Learn_Vue/index.md\"}")
export { comp, data }

if (import.meta.webpackHot) {
  import.meta.webpackHot.accept()
  if (__VUE_HMR_RUNTIME__.updatePageData) {
    __VUE_HMR_RUNTIME__.updatePageData(data)
  }
}

if (import.meta.hot) {
  import.meta.hot.accept(({ data }) => {
    __VUE_HMR_RUNTIME__.updatePageData(data)
  })
}
