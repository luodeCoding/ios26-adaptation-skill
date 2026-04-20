Pod::Spec.new do |s|
  s.name             = 'iOS26Adaptation'
  s.version          = '1.0.1'
  s.summary          = 'iOS 26 SDK adaptation guide, templates, and scanner'
  s.description      = <<-DESC
    iOS26Adaptation is a zero-runtime-impact documentation and tooling package
    for iOS 26 SDK adaptation. It includes:

    - Code templates (Swift & Objective-C) for SceneDelegate migration,
      UIApplication window access, and notification option adaptation
    - Automated project scanner for deprecated APIs
    - Phase-by-phase checklists and testing guides
    - FAQ and troubleshooting documentation

    This package does not compile any code into your app. It is distributed
    as a resource bundle for reference and CI scanning only. Remove it
    anytime after adaptation is complete with zero impact on your project.
  DESC
  s.homepage         = 'https://github.com/luodeCoding/ios26-adaptation-skill'
  s.license          = { :type => 'MIT', :file => 'LICENSE' }
  s.author           = { 'roder' => '' }
  s.source           = { :git => 'https://github.com/luodeCoding/ios26-adaptation-skill.git', :tag => s.version.to_s }

  # Critical: intentionally omit source_files so nothing compiles into the host app
  # s.source_files = ''

  s.resource_bundles = {
    'iOS26Adaptation' => [
      'templates/swift/*',
      'templates/objc/*',
      'scripts/*',
      'docs/*',
      'examples/*',
      '.claude/*',
      'SKILL.md',
      'AGENTS.md',
      'README.md',
      'README.zh.md',
      'CHANGELOG.md'
    ]
  }

  s.platform     = :ios, '12.0'
  s.requires_arc = true
end
