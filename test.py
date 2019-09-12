from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

# Variables
command_server_ip = "https://10.204.217.101:9091/"
username = "admin"
password = "contrail123"
hostname_list = ["nodeg12", "nodeg31", "nodec58", "nodec60", "nodec61"]
mgmt_ip_list = ["10.204.217.52", "10.204.217.71", "10.204.217.98", "10.204.217.100", "10.204.217.101"]
cntl_ip_list = ["77.77.1.20", "77.77.1.30", "77.77.1.11", "77.77.1.21", "77.77.1.31"]
cluster_name = "test"
insecure = False
container_registry = "hub.juniper.net/contrail-nightly"
container_registry_username = "JNPR-Customer200"
container_registry_password = "FSg0vLW^7oM#GZy8Ju*f"
contrail_version = "1909.9"
domain_suffix = "englab.juniper.net"
ntp_server = "10.204.217.158"
default_vrouter_gateway = "77.77.1.100"
contrail_config = {
    "KUBERNETES_PUBLIC_FIP_POOL": "{'project': 'default', 'domain': 'default-domain', 'name': '__fip_pool_public__', "
                                  "'network': '__public__'",
    "KUBERNETES_IP_FABRIC_SUBNETS": "77.77.1.160/27",
    "CLOUD_ORCHESTRATOR:": "kubernetes",
    "CONTROLLER_NODES": "10.204.217.52,10.204.217.71,10.204.217.98",
    "CONTROL_NODES": "77.77.1.20,77.77.1.30,77.77.1.11",
    "KUBERNETES_API_NODES": "77.77.1.20",
    "KUBERNETES_API_SERVER": "77.77.1.20",
    "VROUTER_GATEWAY": "77.77.1.100",
    "LOG_LEVEL": "SYS_DEBUG"
}


# Chrome driver
driver = webdriver.Chrome("driver/chromedriver")

driver.set_page_load_timeout(10)

driver.get(command_server_ip)
driver.find_element_by_id("userName").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_xpath('//*[@id="form-submit"]/span').click()
time.sleep(2)

# Step 1: Inventory
# for i in range(0, len(hostname_list)):
#     # Clicking the Add
#     driver.find_element_by_css_selector('button.jws-btn.jws-btn-primary.jws-btn-sm').send_keys(Keys.ENTER)
#     time.sleep(1)
#     # Selecting "detailed" radio
#     driver.find_element_by_xpath(
#         '/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div/form/div/div[2]/div/fieldset/div[1]/div[3]/label[2]/span/label/span/input') \
#         .click()
#     time.sleep(1)
#
#     driver.find_element_by_xpath('//input[@label="Hostname"]').send_keys(hostname_list[i])
#     driver.find_element_by_css_selector('input[label="Management IP"]').send_keys(mgmt_ip_list[i])
#     driver.find_element_by_css_selector('button.jws-btn.field-array__button-add.jws-btn-text.jws-btn-sm').send_keys(Keys.ENTER)
#
#     time.sleep(1)
#     driver.find_element_by_css_selector('input[placeholder="Enter Name"]').send_keys("eth1")
#     driver.find_element_by_css_selector('input[label="IP Address"]').send_keys(cntl_ip_list[i])
#     driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/div[3]/button[2]').send_keys(Keys.ENTER)
#
#     time.sleep(1)

# Click the next button
driver.find_element_by_xpath('//*[@id="root"]/span/div/div[2]/div/div[2]/div[2]/div[2]/button').send_keys(Keys.ENTER)

# Step 2: Cloud Manager
driver.find_element_by_css_selector('input[label="Cluster Name"]').send_keys(cluster_name)
if insecure:
    driver.find_element_by_xpath('//*[@id="root"]/span/div/div[2]/div/div[2]/div[1]/div/form/div/fieldset/div[2]/div[2]/div[1]/fieldset/div[3]/div[2]/label/label/span[1]/input').send_keys(Keys.ENTER)
    driver.find_element_by_css_selector('input[label="Container Registry"]').clear()
    driver.find_element_by_css_selector('input[label="Container Registry"]').send_keys(container_registry)
else:
    driver.find_element_by_css_selector('input[label="Container Registry"]').clear()
    driver.find_element_by_css_selector('input[label="Container Registry"]').send_keys(container_registry)
    driver.find_element_by_css_selector('input[label="Container Registry Username"]').send_keys(container_registry_username)
    driver.find_element_by_css_selector('input[label="Container Registry Password"]').send_keys(container_registry_password)
driver.find_element_by_css_selector('input[label="Contrail Version"]').clear()
driver.find_element_by_css_selector('input[label="Contrail Version"]').send_keys(contrail_version)
driver.find_element_by_css_selector('input[label="Domain Suffix"]').clear()
driver.find_element_by_css_selector('input[label="Domain Suffix"]').send_keys(domain_suffix)
driver.find_element_by_css_selector('input[label="NTP Server"]').send_keys(ntp_server)
driver.find_element_by_css_selector('input[label="Default Vrouter Gateway"]').send_keys(default_vrouter_gateway)

# Encapsulation priority
# element = driver.find_element_by_class_name('contrail-wizard-content')
# driver.execute_script("arguments[0].scrollTo(0,500)", element)
# driver.find_element_by_xpath("//label[text()='Encapsulation Priority']/following-sibling::div[@class]").click()
# time.sleep(1)
# driver.find_element_by_xpath("//li[text()='VXLAN,MPLSoUDP,MPLSoGRE']").click()
# time.sleep(2)

# Contrail Configuration
# element = driver.find_element_by_class_name('arrow')
# driver.execute_script("arguments[0].click();", element)
# time.sleep(1)
# # Clicking the Add button
# driver.find_element_by_css_selector('.jws-btn.field-array__button-add.jws-btn-text.jws-btn-sm').send_keys(Keys.ENTER)
#
# for i,(k,v) in enumerate(contrail_config.items()):
#     xpath_key = '//input[@id[contains(.,"contrailSchema_contrail_configuration_{}_key")]]'.format(i)
#     xpath_value = '//input[@id[contains(.,"contrailSchema_contrail_configuration_{}_value")]]'.format(i)
#     driver.find_element_by_xpath(xpath_key).send_keys(k)
#     driver.find_element_by_xpath(xpath_value).send_keys(v)
#     if i < len(contrail_config)-1:
#         driver.find_element_by_css_selector('.jws-btn.field-array__button-add.jws-btn-text.jws-btn-sm').send_keys(
#             Keys.ENTER)

driver.find_element_by_css_selector(".jws-btn.contrail-wizard-proceed.jws-btn-primary").send_keys(Keys.ENTER)

# Step 3
time.sleep(1)
# Clicking the arrow button of available servers to assign control nodes
for i, server in enumerate(driver.find_elements_by_xpath("//i[@class='jws jws-arrowTransfer_right jws-icon']/parent::button")):
    server.send_keys(Keys.ENTER)
    if i == 2:
        break
for i, combo in enumerate(driver.find_elements_by_xpath("//div[@role='combobox']")):
    combo.click()
    alarm_x_path = "(//li[text()='contrail_analytics_alarm_node'])[{}]".format(i+1)
    snmp_x_path = "(//li[text()='contrail_analytics_snmp_node'])[{}]".format(i+1)
    driver.find_element_by_xpath(alarm_x_path).click()
    driver.find_element_by_xpath(snmp_x_path).click()
    # for j, alarm in enumerate(driver.find_elements_by_xpath("//li[text()='contrail_analytics_alarm_node']")):
    #     if j == i:
    #         alarm.click()
    # for k, snmp in enumerate(driver.find_elements_by_xpath("//li[text()='contrail_analytics_snmp_node']")):
    #     if k == i:
    #         snmp.click()
