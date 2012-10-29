<?php

/**
 * (c) 2004-2007 Linbox / Free&ALter Soft, http://linbox.com
 * (c) 2007-2012 Mandriva, http://www.mandriva.com
 *
 * This file is part of Mandriva Management Console (MMC).
 *
 * MMC is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * MMC is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with MMC.  If not, see <http://www.gnu.org/licenses/>.
 */

/**
 * shorewall module declaration
 */

$mod = new Module("shorewall");
$mod->setVersion("2.4.3");
$mod->setRevision('');
$mod->setDescription(_T("Firewall", "shorewall"));
$mod->setAPIVersion("0:0:0");

$submod = new SubModule("shorewall", _T("Firewall", "shorewall"));
$submod->setDefaultPage("shorewall/shorewall/internal_fw");
$submod->setImg('img/navbar/load');
$submod->setPriority(20000);

/* Add the page to the module */
$page = new Page("internal_fw", _T("Internal → Server", "shorewall"));
$submod->addPage($page);

$page = new Page("ajax_internal_fw");
$page->setOptions(array("visible" => False, "AJAX" => True));
$submod->addPage($page);

$page = new Page("delete_internal_fw_rule");
$page->setOptions(array("visible" => False, "AJAX" => True));
$submod->addPage($page);

$page = new Page("external_fw", _T("External → Server", "shorewall"));
$submod->addPage($page);

$page = new Page("ajax_external_fw");
$page->setOptions(array("visible" => False, "AJAX" => True));
$submod->addPage($page);

$page = new Page("delete_external_fw_rule");
$page->setOptions(array("visible" => False, "AJAX" => True));
$submod->addPage($page);

$page = new Page("internal_external", _T("Internal → External", "shorewall"));
$submod->addPage($page);

$page = new Page("ajax_internal_external");
$page->setOptions(array("visible" => False, "AJAX" => True));
$submod->addPage($page);

$page = new Page("external_internal", _T("External → Internal", "shorewall"));
$submod->addPage($page);

$page = new Page("ajax_external_internal");
$page->setOptions(array("visible" => False, "AJAX" => True));
$submod->addPage($page);

$page = new Page("delete_external_internal_rule");
$page->setOptions(array("visible" => False, "AJAX" => True));
$submod->addPage($page);

$page = new Page("policies", _T("Firewall policies"));
$submod->addPage($page);

$page = new Page("masquerade", _T("NAT"));
$submod->addPage($page);

$page = new Page("ajax_masquerade");
$page->setOptions(array("visible" => False, "AJAX" => True));
$submod->addPage($page);

$page = new Page("delete_masquerade_rule");
$page->setOptions(array("visible" => False, "AJAX" => True));
$submod->addPage($page);

$mod->addSubmod($submod);

$MMCApp =& MMCApp::getInstance();
$MMCApp->addModule($mod);

?>
