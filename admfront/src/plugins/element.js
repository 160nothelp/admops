import Vue from 'vue'
import {
  Form, FormItem, Input, Button, Message, Container,
  Header, Aside, Main, Menu, MenuItem, Submenu, Breadcrumb,
  BreadcrumbItem, Card, Row, Col, Table, TableColumn, Dialog, Pagination, Switch
  , MessageBox, Tooltip, DropdownMenu, DropdownItem, Dropdown, Tree, Scrollbar
} from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css' // UI组件样式

Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Button)
Vue.use(Container)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Header)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItem)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Card)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Dialog)
Vue.use(Pagination)
Vue.use(Switch)
Vue.use(Tooltip)
Vue.use(Dropdown)
Vue.use(DropdownMenu)
Vue.use(DropdownItem)
Vue.use(Tree)
Vue.use(Scrollbar)

let messageInstance = null;
const resetMessage = (options) => {
    if(messageInstance) {
        messageInstance.close() //关闭
    }
    messageInstance = Message(options)
};
['error','success','info','warning'].forEach(type => {
    resetMessage[type] = options => {
        if(typeof options === 'string') {
            options = {
                message:options
            }
        }
        options.type = type
        return resetMessage(options)
    }
})

Vue.prototype.$message = resetMessage
Vue.prototype.$msgbox = MessageBox
