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
control_list = []
compute_list = []
k8s_master_nodes = []
kubemanager_nodes = []
k8s_nodes = []

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

for node, value in instances_data['instances'].items():
    if 'control' in value['roles']:
        control_list.append(node)
        print("Control nodes:",node)
    if 'vrouter' in value['roles']:
        compute_list.append(node)
        print("Compute nodes:",node)
    if 'k8s_master' in value['roles']:
        k8s_master_nodes.append(node)
        print("Kube master:",node)
    if 'kubemanager' in value['roles']:
        kubemanager_nodes.append(node)
        print("kubemanager:",node)
    if 'k8s_node' in value['roles']:
        k8s_nodes.append(node)
        print("k8s_node:",node)

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
    # driver.find_element_by_css_selector('.jws-btn.field-array__button-add.jws-btn-text.jws-btn-sm').send_keys(
    #     Keys.ENTER)

    # for i, (k, v) in enumerate(contrail_config.items()):
    #     xpath_key = '//input[@id[contains(.,"contrailSchema_contrail_configuration_{}_key")]]'.format(i)
    #     xpath_value = '//input[@id[contains(.,"contrailSchema_contrail_configuration_{}_value")]]'.format(i)
    #     driver.find_element_by_xpath(xpath_key).send_keys(k)
    #     driver.find_element_by_xpath(xpath_value).send_keys(str(v))
    #     if i < len(contrail_config) - 1:
    #         driver.find_element_by_css_selector('.jws-btn.field-array__button-add.jws-btn-text.jws-btn-sm').send_keys(
    #             Keys.ENTER)


# Step 7:Control nodes
def control_nodes():
    # Select high availability mode
    driver.find_element_by_xpath("//span[text()='High availability mode']/preceding-sibling::span/input").click()
    time.sleep(1)
    # Clicking each control node and removing alarm and snmp components
    j = 1
    for control in control_list:
        arrow_xpath = "//div[@title='{}']/following::i[@class='jws jws-arrowTransfer_right jws-icon']/parent::button"\
            .format(control)
        # Clicking each control's arrow key
        driver.find_element_by_xpath(arrow_xpath).send_keys(Keys.ENTER)
        combo_xpath = "(//div[@role='combobox'])[{}]".format(j)
        combo_xpath = driver.find_element_by_xpath(combo_xpath)
        alarm_x_path = "(//li[@title='contrail_analytics_alarm_node']//span)[{}]".format(j)
        snmp_x_path = "(//li[@title='contrail_analytics_snmp_node']//span)[{}]".format(j)
        time.sleep(1)
        driver.find_element_by_xpath(alarm_x_path).click()
        time.sleep(1)
        driver.execute_script("arguments[0].scrollTo(0,500)", combo_xpath)
        # driver.find_element_by_xpath(snmp_x_path).click()
        time.sleep(1)
        j = j + 1


# Step 8:Orchestrator Nodes 
def orchestrator_nodes():
    arrow_xpath = "//div[@title='{}']/following::i[@class='jws jws-arrowTransfer_right jws-icon']/parent::button"
    combo_xpath = "(//div[@role='combobox'])[{}]"
    driver.find_element_by_css_selector(".ant-select-selection__rendered").click()
    time.sleep(1)
    driver.find_element_by_xpath("//li[text()='Kubernetes']").click()

    j = 2
    # import pdb;pdb.set_trace()
    # K8S Master
    for master in k8s_master_nodes:
        arrow = arrow_xpath.format(master)
        # Clicking master's arrow
        driver.find_element_by_xpath(arrow).send_keys(Keys.ENTER)
        combo = combo_xpath.format(j)
        driver.find_element_by_xpath(combo).click()
        time.sleep(1)
        # Click kubernetes_node to remove it
        node_x_path = "(//li[text()='kubernetes_node'])[{}]".format(j-1)
        driver.find_element_by_xpath(node_x_path).click()
        j = j + 1

    # Kubemanager
    for manager in kubemanager_nodes:
        if manager not in k8s_master_nodes:
            arrow = arrow_xpath.format(manager)
            # Clicking manager's arrow
            driver.find_element_by_xpath(arrow).send_keys(Keys.ENTER)
            combo = combo_xpath.format(j)
            driver.find_element_by_xpath(combo).click()
            time.sleep(1)
            # Click master and node to remove it
            master_node_x_path = "(//li[text()='kubernetes_master_node'])[{}]".format(j-1)
            driver.find_element_by_xpath(master_node_x_path).click()
            node_x_path = "(//li[text()='kubernetes_node'])[{}]".format(j-1)
            driver.find_element_by_xpath(node_x_path).click()
            j = j + 1

    # K8s nodes
    for node in k8s_nodes:
        arrow = arrow_xpath.format(node)
        # Clicking kubernetes node's arrow
        driver.find_element_by_xpath(arrow).send_keys(Keys.ENTER)
        combo = combo_xpath.format(j)
        driver.find_element_by_xpath(combo).click()
        time.sleep(1)
        # Clicking master and manager to remove it
        master_node_x_path = "(//li[text()='kubernetes_master_node'])[{}]".format(j-1)
        driver.find_element_by_xpath(master_node_x_path).click()
        kube_manager_x_path = "(//li[text()='kubernetes_kubemanager_node'])[{}]".format(j-1)
        driver.find_element_by_xpath(kube_manager_x_path).click()
        j = j + 1


# Step 9:Compute nodes
def compute_nodes():
    time.sleep(1)
    arrow_xpath = "//div[@title='{}']/following::i[@class='jws jws-arrowTransfer_right jws-icon']/parent::button"
    vrouter_xpath = "(//input[@label='Default Vrouter Gateway'])[{}]"
    j = 1
    for compute in compute_list:
        arrow = arrow_xpath.format(compute)
        driver.find_element_by_xpath(arrow).send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element_by_xpath(vrouter_xpath.format(j)).send_keys(
            default_vrouter_gateway)
        j = j + 1
    next()


if __name__ == '__main__':
    # inventory()
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
    print("Touching the combobox is having problem")
