# ui_automation

* Solution for the below problem:
    * selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <span data-react-id="...">contrail_analytics_alarm_node</span> is not clickable at point (949, 374). Other element would receive the click: <li unselectable="unselectable" class="ant-select-dropdown-menu-item-selected ant-select-dropdown-menu-item" role="menuitem" aria-selected="true" aria-disabled="false" style="user-select: none;">...</li>
    * This appears if that element is hidden or different element is selected
    * Try other element like the parent or div 
    * Approach of ancestor li instead of span
    * Another approach of execute_script
    * Best approach: Think of using js console in browser and follow. See doc in Evernote
    