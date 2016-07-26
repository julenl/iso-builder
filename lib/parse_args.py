#! /usr/bin/env python

def ib_parser(script_dir):
    import os,sys
    import re
    #print cmd_args

    print "  Running iso-builder as:"
    print " ".join(sys.argv)
    print 
  
    import argparse
    parser = argparse.ArgumentParser(
        description='iso-builder is a python script for building customized/self installing GNU/Linux ISO files. It extracts an original ISO file (def. Ubuntu) copies the content, adds kickstart files, edits the menus and rebuilds the content into a new ISO. Running the script without arguments produces a new self installed ISO with default options.',
        epilog='Example: iso-builder --out_iso_name My_Ubuntu_16.04.iso ' ,
        add_help=False)

    group = parser.add_argument_group("General options")
    group.add_argument("-h","--help", action="help",
                        help="Show this help message and exit")
    group.add_argument("-v","--version", action='version', version='%(prog)s 0.1',
                        help="Show version and exit")
    group.add_argument("-y","--yes", action='store_true',
                        help="Answer 'Y' if prompted whether to overwrite the ks template.")
    group.add_argument("-t","--test", action='store_true',
                        help="Test resulting ISO by installing it into a KVM Virtual Machine.")



    group = parser.add_argument_group("Options for building the ISO file")

    group.add_argument("--ks_file",
                        help="Name of the kickstart template file. Def.: ks_file_template")
    group.add_argument("--template_dir",
                        help="Directory containing kickstart templates. Def.: ~/ib_templates")
    group.add_argument("--out_iso_name",
                        help="Name of the custom ISO to be generated. Def.: custom.iso")
    group.add_argument("--iso_dir",
                        help="Directory where original ISO files are stored. Def.: ~/ISOS")
    group.add_argument("--use_template",
                        help="Use this kickstart file as template. Def.: $PWD/basic_ks_file")
    group.add_argument("--loc_kickstart_dir",
                        help="Directory where kickstart templates are stored. Def.: ~/ib_templates")
    group.add_argument("--template_name",
                        help="Name for the new kickstart template generated at the --loc_kickstart_dir. Def.: ks.cfg")
    group.add_argument("--iso_name",
                        help="Name of the original ISO file. Def.: ubuntu-16.04-server-amd64.iso")
    group.add_argument("--get_os",choices=['ubuntu-14.04.4', 'ubuntu-15.10', 'ubuntu-16.04', 'debian-8.5.0'],
                        help="Get server ISO for this Operative System. Def.: 'ubuntu-16.04'")
    group.add_argument("--tmp_mnt_dir",
                        help="Temporal directory to mount the original ISO file. Def.: /tmp/tmp_mnt_dir/")
    group.add_argument("--tmp_edit_dir",
                        help="Temporal directory to edit the ISO file. Def.: /tmp/tmp_edit_dir/")
    group.add_argument("--out_iso_dir",
                        help="Directory to store the generated ISO file. Def.: ~/")
    group.add_argument("--cp_to_iso",
                        help="Copy this file/folder to the ISO root directory. Def.: None")


    group = parser.add_argument_group("Target system options")

    group.add_argument("--root_password",
                        help="Enable and set the root password for the target system. Def.: 'ChangeMe'")
    group.add_argument("--user_password",
                        help="Create a username with an associated password. Def.: 'user:ChangeMe'")

    group.add_argument("--post_script",
                        help="Script file to run on the post-install section. Def.: None")
    group.add_argument("--post_script_nc",
                        help="Content of post-script --nochroot (Ex.: cp -r /target/media/cdrom/my_folder /target/root/). Def.: None")
    group.add_argument("--keyboard",
                        help="Keyboard layout. Def.: 'us'",nargs=1)
    group.add_argument("--language",
                        help="System language. Def.: 'us'",nargs=1)
    group.add_argument("--timezone",
                        help="Time zone. Def.: 'Europe/Berlin --isUtc'",nargs=1)


    group = parser.add_argument_group("Target system networking")

    group.add_argument("--hostname",
                        help="Set hostname for the target system. Def.: iso-builder")
    group.add_argument("--device",
                        help="Network device/interface name. Def.: eth0")
    group.add_argument("--bootproto", choices=['dhcp','static'],
                        help="Set network boot protocol. Def.: 'dhcp'")
    group.add_argument("--ip",
                        help="Set IP address for the target. Def.: '10.0.0.11'")
    group.add_argument("--netmask",
                        help="Set netmask for the target. Def.: '255.255.255.0'")
    group.add_argument("--gateway",
                        help="Set network gateway address. Def.: (--ip).'1'")
    group.add_argument("--dns",
                        help="Set DNS address. Def.: (--ip).'1'")
    #group.add_argument("--network",
    #                    help="Setup network. Def.: 'network --bootproto=dhcp --device=eth0'. \nExample: 'network --bootproto=static --device=eth0  --ip=10.0.0.11 --netmask=255.255.255.0 --gateway=10.0.0.1 --nameserver=10.0.0.1 --activate --hostname=ubuntu'",nargs=1)




    args=parser.parse_args()
 
    ## This dictionary stores the vars to pass to the main script 
    args_dict={}

    ## This dictionary stores key:values for substituting on
    ## the kickstart file
    ks_values_dict={}    


    ## YES option
    args_dict['ans_yes']=args.yes

    ## test option
    args_dict['test_vm']=args.test

    ## Output ISO name 
    if not args.out_iso_name:
       args.out_iso_name = "custom.iso"
    if not args.out_iso_name.endswith(('.iso','.ISO')):
       args.out_iso_name = args.out_iso_name + '.iso'
    args_dict['out_iso_name']=args.out_iso_name

    ## ISO directory
    if not args.iso_dir:
       args.iso_dir = os.path.expanduser("~") + '/ISOS/'
    args_dict['iso_dir']=args.iso_dir

    ## Use this kickstart file as template
    if not args.use_template:
       if os.path.exists("/usr/lib/iso-builder/ks_template.cfg"):
          args.use_template = '/usr/lib/iso-builder/ks_template.cfg'
       else:
          #script_dir=os.path.dirname(os.path.realpath(__file__))
          args.use_template = script_dir + 'ks_template.cfg'
    args_dict['use_template']=args.use_template

    ## Local kicstart template directory
    if not args.loc_kickstart_dir:
       args.loc_kickstart_dir = os.path.expanduser("~") + '/ib_templates'
    args_dict['loc_kickstart_dir']=args.loc_kickstart_dir

    ## Name for the new kickstart template stored in loc_kickstart_dir
    if not args.template_name:
       args.template_name = 'ks.cfg'
    args_dict['template_name']=args.template_name

    ## original ISO name
    if not args.iso_name:
       if not args.get_os:
           args.iso_name = 'ubuntu-16.04-server-amd64.iso'
    args_dict['iso_name']=args.iso_name

    ## get/use the original iso for this Operative System/version
    if not args.get_os:
       args.get_os = 'ubuntu-16.04'
    args_dict['get_os']=args.get_os

    ## TMP Mount dir
    if not args.tmp_mnt_dir:
       args.tmp_mnt_dir = '/tmp/tmp_mnt_dir/'
    args_dict['tmp_mnt_dir']=args.tmp_mnt_dir

    ## TMP Edit dir
    if not args.tmp_edit_dir:
       args.tmp_edit_dir = '/tmp/tmp_edit_dir/'
    args_dict['tmp_edit_dir']=args.tmp_edit_dir

    ## Out ISO dir
    if not args.out_iso_dir:
       args.out_iso_dir = os.path.expanduser("~") + '/'
    args_dict['out_iso_dir']=args.out_iso_dir

    if args.cp_to_iso:
       if os.path.exists(args.cp_to_iso):
           args_dict['cp_to_iso']= args.cp_to_iso
           fname=os.path.split(args.cp_to_iso)[1]
           cmd= "cp -r /target/media/cdrom/" + fname + " /target/root/" 
           ks_values_dict[re.compile('## ISOBUILDER-CP_TO_ISO')]= cmd
       else:
           sys.exit("ERROR: the file/folder " + args.cp_to_iso + ' could not be found.')


    #########################################################
    ## These are the "Target system options"
    ## Careful!! Unlike the General and ISO building options,
    ## if these options are unset, we won't set them.
    ## This allows to use custom kickstart file templates
    ## without overwriting them.
    ## Values are stored as 'search regex key':'line in kickstart'
    


    ## Root password
    if args.root_password and len(args.root_password) > 2:
       ks_values_dict[re.compile('^rootpw .*')]= 'rootpw ' + args.root_password

    ## User and password
    if args.user_password and len(args.user_password.split(':')) == 2:
       user=args.user_password.split(':')[0]
       password=args.user_password.split(':')[1]
       ks_values_dict[re.compile('^user .*')]= 'user ' + user + ' --fullname "Ubuntu user" --password ' + password

    if args.post_script:
       if os.path.isfile(args.post_script):
           p_script=open(args.post_script,"r").read()
           print "Including the following script as %post"
           print "============================================="
           print p_script
           print "============================================="
           ks_values_dict[re.compile('## ISOBUILDER-POST-SCRIPT.*')]= p_script 
       else:
           sys.exit("ERROR: the script file " + args.post_script + ' could not be found.')


    if args.post_script_nc:
       if os.path.isfile(args.post_script_nc):
           p_script_nc=open(args.post_script_nc,"r").read()
           print "Including the following script as %post --nochroot"
           print "============================================="
           print p_script_nc
           print "============================================="
           ks_values_dict[re.compile('## ISOBUILDER-POST-SCRIPT-NC.*')]= p_script_nc 
       else:
           sys.exit("ERROR: the script file " + args.post_script_nc + ' could not be found.')







    ##########
    ## Network
        

    ## Hostname
    if not args.hostname:
       args.hostname="ubuntu"

    if not args.device:
       args.device="eth0"

    static_opts=[args.ip,args.dns,args.gateway,args.netmask]
    if args.bootproto:

        if args.bootproto == 'dhcp':
           print "dhcp"
           if any(static_opts):
              sys.exit("ERROR: the 'dhcp' option does not require to set the IP, gateway, nameserver or netmask")


        if args.bootproto == 'static':
           if not args.ip:
              print "WARNING: static network configuration was selected, but no IP was set. Setting it to 10.0.0.11"
              args.ip="10.0.0.11"

           if not args.netmask:
              args.netmask = "255.255.255.0"
              print "WARNING: static network configuration was selected, but no gateway was set. Setting it to: " + args.netmask
 
           ## If gateway and/or nameserver are not set, the will be the same as the IP
           ## but with the last octet set to 1
           ip_pref=".".join(args.ip.split(".")[0:3])
           if not args.gateway:
              args.gateway = ip_pref + ".1"
              print "WARNING: static network configuration was selected, but no gateway was set. Setting it to: " + args.gateway
 
           if not args.dns:
              args.dns = ip_pref + ".1"
              print "WARNING: static network configuration was selected, but no nameserver was set. Setting it to: " + args.dns
 
           ## Build the long string for the network setup on the kickstart file
           ks_values_dict[re.compile('^network .*')]=  \
           'network --activate ' + \
           ' --bootproto=' + args.bootproto + \
           ' --device ' + args.device + \
           ' --ip='+ args.ip + \
           ' --netmask=' + args.netmask + \
           ' --gateway=' + args.gateway + \
           ' --nameserver=' + args.dns + \
           ' --activate --hostname=' + args.hostname

       #ks_values_dict[re.compile('^rootpw .*')]= 'rootpw ' + args.root_password




    args_dict['ks_values_dict']=ks_values_dict

    return args_dict




