from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import yaml

with open('instances_command_folder/instances.yml') as f:
    instances_data = yaml.safe_load(f)

with open('instances_command_folder/command_servers.yml') as f:
    command_data = yaml.safe_load(f)

# Variables
username = "admin"
password = "contrail123"
cluster_name = "test_ui2"
domain_suffix = "englab.juniper.net"

command_server_ip = "https://" + command_data['command_servers']['server1']['ip'] + ":9091"
hostname_list = []
mgmt_ip_list = []
cntl_ip_list = []

for i in instances_data['instances']:
    hostname_list.append(i)
for k,v in instances_data['instances'].items():
    mgmt_ip_list.append(v['ip'])
for k,v in instances_data['control_data'].items():
    cntl_ip_list.append(v['ctrldata_ip'])

insecure = instances_data['REGISTRY_PRIVATE_INSECURE']
container_registry = instances_data['CONTAINER_REGISTRY']

if not insecure:
    container_registry_username = instances_data['CONTAINER_REGISTRY_USERNAME']
    container_registry_password = instances_data['CONTAINER_REGISTRY_PASSWORD']

contrail_version = instances_data['contrail_configuration']['CONTRAIL_VERSION']
ntp_server = instances_data['provider_config']['bms']['ntpserver']
default_vrouter_gateway = instances_data['contrail_configuration']['VROUTER_GATEWAY']
contrail_config = instances_data['contrail_configuration']



# Chrome driver
driver = webdriver.Chrome("driver/chromedriver")

driver.set_page_load_timeout(25)

driver.get(command_server_ip)
driver.find_element_by_id("userName").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_xpath('//*[@id="form-submit"]/span').click()
time.sleep(2)


# Step 1: Inventory
def inventory():
    for i in range(0, len(hostname_list)):
        # Click Add
        driver.find_element_by_xpath("//span[text()='Add']/parent::button").send_keys(Keys.ENTER)
        time.sleep(1)
        # Selecting "detailed" radio
        driver.find_element_by_xpath("//span[text()='Detailed']//preceding-sibling::label/span/input").click()
        time.sleep(1)

        driver.find_element_by_xpath("//input[@label='Hostname']").send_keys(hostname_list[i])
        driver.find_element_by_css_selector('input[label="Management IP"]').send_keys(mgmt_ip_list[i])
        driver.find_element_by_xpath("//span[text()='+ Add']/parent::button").send_keys(Keys.ENTER)

        time.sleep(1)
        driver.find_element_by_css_selector('input[placeholder="Enter Name"]').send_keys("eth1")
        driver.find_element_by_css_selector('input[label="IP Address"]').send_keys(cntl_ip_list[i])
        driver.find_element_by_xpath("//span[text()='Create']/parent::button").send_keys(Keys.ENTER)

        time.sleep(1)


# Click the next button
def next():
    driver.find_element_by_xpath("//span[text()='Next']/parent::button").send_keys(Keys.ENTER)


# Step 2: Cloud Manager
def cloud_manager():
    driver.find_element_by_css_selector('input[label="Cluster Name"]').send_keys(cluster_name)
    if insecure:
        driver.find_element_by_xpath("//span[text()='Insecure']/preceding-sibling::span/input").click()
        driver.find_element_by_css_selector('input[label="Container Registry"]').clear()
        driver.find_element_by_css_selector('input[label="Container Registry"]').send_keys(container_registry)
    else:
        driver.find_element_by_css_selector('input[label="Container Registry"]').clear()
        driver.find_element_by_css_selector('input[label="Container Registry"]').send_keys(container_registry)
        driver.find_element_by_css_selector('input[label="Container Registry Username"]').send_keys(
            container_registry_username)
        driver.find_element_by_css_selector('input[label="Container Registry Password"]').send_keys(
            container_registry_password)
    driver.find_element_by_css_selector('input[label="Contrail Version"]').clear()
    driver.find_element_by_css_selector('input[label="Contrail Version"]').send_keys(contrail_version)
    driver.find_element_by_css_selector('input[label="Domain Suffix"]').clear()
    driver.find_element_by_css_selector('input[label="Domain Suffix"]').send_keys(domain_suffix)
    driver.find_element_by_css_selector('input[label="NTP Server"]').send_keys(ntp_server)
    driver.find_element_by_css_selector('input[label="Default Vrouter Gateway"]').send_keys(default_vrouter_gateway)

    # Encapsulation priority
    element = driver.find_element_by_class_name('contrail-wizard-content')
    driver.execute_script("arguments[0].scrollTo(0,500)", element)
    driver.find_element_by_xpath("//label[text()='Encapsulation Priority']/following-sibling::div[@class]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//li[text()='VXLAN,MPLSoUDP,MPLSoGRE']").click()

    # Contrail Configuration
    element = driver.find_element_by_class_name('arrow')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(1)
    # Clicking the Add button
    driver.find_element_by_css_selector('.jws-btn.field-array__button-add.jws-btn-text.jws-btn-sm').send_keys(
        Keys.ENTER)

    for i, (k, v) in enumerate(contrail_config.items()):
        xpath_key = '//input[@id[contains(.,"contrailSchema_contrail_configuration_{}_key")]]'.format(i)
        xpath_value = '//input[@id[contains(.,"contrailSchema_contrail_configuration_{}_value")]]'.format(i)
        driver.find_element_by_xpath(xpath_key).send_keys(k)
        driver.find_element_by_xpath(xpath_value).send_keys(str(v))
        if i < len(contrail_config) - 1:
            driver.find_element_by_css_selector('.jws-btn.field-array__button-add.jws-btn-text.jws-btn-sm').send_keys(
                Keys.ENTER)

# Need to change from here
# Step 7:Control nodes
def control_nodes():
    # Select high availability mode
    driver.find_element_by_xpath("//span[text()='High availability mode']/preceding-sibling::span/input").click()
    time.sleep(1)
    # Clicking the arrow button of available servers to assign control nodes
    for i, server in enumerate(
            driver.find_elements_by_xpath("//i[@class='jws jws-arrowTransfer_right jws-icon']/parent::button")):
        server.send_keys(Keys.ENTER)
        if i == 2:
            break
    for i, combo in enumerate(driver.find_elements_by_xpath("//div[@role='combobox']")):
        combo.click()
        alarm_x_path = "(//li[text()='contrail_analytics_alarm_node'])[{}]".format(i + 1)
        time.sleep(1)
        snmp_x_path = "(//li[text()='contrail_analytics_snmp_node'])[{}]".format(i + 1)
        time.sleep(1)
        driver.find_element_by_xpath(alarm_x_path).click()
        driver.find_element_by_xpath(snmp_x_path).click()


# Step 8:Orchestrator Nodes Not working as expected
def orchestrator_nodes():
    driver.find_element_by_css_selector(".ant-select-selection__rendered").click()
    time.sleep(1)
    driver.find_element_by_xpath("//li[text()='Kubernetes']").click()
    # Clicking the arrow button of available servers to assign roles
    for i, server in enumerate(
            driver.find_elements_by_xpath("//i[@class='jws jws-arrowTransfer_right jws-icon']/parent::button")):
        server.send_keys(Keys.ENTER)
    for i, combo in enumerate(driver.find_elements_by_xpath("//div[@role='combobox']")):
        if i == 0:
            continue
        # clicking the li's which are not needed
        # Optimize the below condition
        if len(hostname_list) == 4:
            if i == 1:
                combo.click()
                master_node_x_path = "(//li[text()='kubernetes_master_node'])[{}]".format(i)
                driver.find_element_by_xpath(master_node_x_path).click()
                kube_manager_x_path = "(//li[text()='kubernetes_kubemanager_node'])[{}]".format(i)
                driver.find_element_by_xpath(kube_manager_x_path).click()
            elif i == 2 or i == 3:
                combo.click()
                master_node_x_path = "(//li[text()='kubernetes_master_node'])[{}]".format(i)
                driver.find_element_by_xpath(master_node_x_path).click()
                node_x_path = "(//li[text()='kubernetes_node'])[{}]".format(i)
                driver.find_element_by_xpath(node_x_path).click()
            else:
                combo.click()
                kube_manager_x_path = "(//li[text()='kubernetes_node'])[{}]".format(i)
                driver.find_element_by_xpath(kube_manager_x_path).click()
        else:
            if i == 1 or i == 2:
                combo.click()
                master_node_x_path = "(//li[text()='kubernetes_master_node'])[{}]".format(i)
                driver.find_element_by_xpath(master_node_x_path).click()
                kube_manager_x_path = "(//li[text()='kubernetes_kubemanager_node'])[{}]".format(i)
                driver.find_element_by_xpath(kube_manager_x_path).click()
            elif i == 3 or i == 4:
                combo.click()
                master_node_x_path = "(//li[text()='kubernetes_master_node'])[{}]".format(i)
                driver.find_element_by_xpath(master_node_x_path).click()
                node_x_path = "(//li[text()='kubernetes_node'])[{}]".format(i)
                driver.find_element_by_xpath(node_x_path).click()
            else:
                combo.click()
                kube_manager_x_path = "(//li[text()='kubernetes_node'])[{}]".format(i)
                driver.find_element_by_xpath(kube_manager_x_path).click()

# Step 9:Compute nodes
def compute_nodes():
    time.sleep(1)
    driver.find_element_by_xpath("(//i[@class='jws jws-arrowTransfer_right jws-icon']/parent::button)[1]").send_keys(Keys.ENTER)
    time.sleep(1)
    driver.find_element_by_xpath("(//input[@label='Default Vrouter Gateway'])[1]").send_keys(default_vrouter_gateway)
    if len(hostname_list) == 5:
        driver.find_element_by_xpath("(//i[@class='jws jws-arrowTransfer_right jws-icon']/parent::button)[2]").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element_by_xpath("(//input[@label='Default Vrouter Gateway'])[2]").send_keys(default_vrouter_gateway)
    next()

if __name__ == '__main__':
    inventory()
    next()
    cloud_manager()
    next()
    control_nodes()
    next()
    orchestrator_nodes()
    next()
    compute_nodes()
    next()
    next()
    next()
