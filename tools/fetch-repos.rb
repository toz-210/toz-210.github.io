# frozen_string_literal: true

# 빌드 전에 실행: _data/blog_categories.yml 의 각 저장소 정보를
# GitHub API로 읽어서 _data/repo_info.json 으로 저장한다.
# 다른 저장소에는 읽기만 하고 아무것도 쓰지 않는다.

require "json"
require "net/http"
require "time"
require "uri"
require "yaml"

OWNER = "toz-210"
ROOT = File.expand_path("..", __dir__)
CATEGORIES = File.join(ROOT, "_data", "blog_categories.yml")
OUTPUT = File.join(ROOT, "_data", "repo_info.json")

def api_get(path, accept: "application/vnd.github+json")
  uri = URI("https://api.github.com#{path}")
  req = Net::HTTP::Get.new(uri)
  req["Accept"] = accept
  req["User-Agent"] = "toz-210-blog-build"
  req["X-GitHub-Api-Version"] = "2022-11-28"
  token = ENV["GITHUB_TOKEN"]
  req["Authorization"] = "Bearer #{token}" if token && !token.empty?

  res = Net::HTTP.start(uri.host, uri.port, use_ssl: true, open_timeout: 10, read_timeout: 20) do |http|
    http.request(req)
  end
  return nil unless res.is_a?(Net::HTTPSuccess)

  accept.end_with?("html") ? res.body.force_encoding("UTF-8") : JSON.parse(res.body)
rescue StandardError => e
  warn "  ! #{path}: #{e.class} #{e.message}"
  nil
end

# GitHub이 렌더링한 README HTML을 블로그 안에서 안전하게 쓰도록 정리
def tidy_readme(html, repo, branch)
  return nil if html.nil? || html.strip.empty?

  base = "https://github.com/#{OWNER}/#{repo}"
  html = html.dup
  # GitHub 화면용 레이아웃 클래스 제거 (블로그 카드 안에서 여백이 틀어지지 않게)
  html.gsub!(" container-lg", "")
  # 제목 옆에 붙는 GitHub 링크 아이콘은 빼고, 이동용 id만 남김
  html.gsub!(%r{<a id="(user-content-[^"]*)" class="anchor"[^>]*>.*?</a>}m) { %(<span id="#{Regexp.last_match(1)}"></span>) }
  # 목차 같은 문서 내부 링크(#제목)를 GitHub이 붙인 id(user-content-제목)에 맞춤
  html.gsub!(/href="#(?!user-content-)/, 'href="#user-content-')
  # 상대 경로 링크는 저장소 페이지로 연결
  html.gsub!(%r{href="(?!https?://|#|mailto:)/?([^"]*)"}) { %(href="#{base}/blob/#{branch}/#{Regexp.last_match(1)}") }
  # 상대 경로 이미지는 원본 파일 주소로 연결
  html.gsub!(%r{src="(?!https?://|data:)/?([^"]*)"}) do
    %(src="https://raw.githubusercontent.com/#{OWNER}/#{repo}/#{branch}/#{Regexp.last_match(1)}")
  end
  html
end

categories = YAML.safe_load(File.read(CATEGORIES, encoding: "UTF-8")) || []
info = {}

categories.each do |c|
  repo = c["repo"]
  next if repo.nil? || repo.empty?

  puts "- #{repo}"
  meta = api_get("/repos/#{OWNER}/#{repo}")
  if meta.nil?
    info[repo] = { "found" => false, "url" => "https://github.com/#{OWNER}/#{repo}" }
    next
  end

  branch = meta["default_branch"] || "main"
  commits = api_get("/repos/#{OWNER}/#{repo}/commits?per_page=5") || []
  commits = [] unless commits.is_a?(Array)

  info[repo] = {
    "found" => true,
    "name" => meta["name"],
    "url" => meta["html_url"],
    "description" => meta["description"],
    "language" => meta["language"],
    "pushed_at" => meta["pushed_at"],
    "empty" => commits.empty?,
    "commits" => commits.map do |cm|
      {
        "message" => cm.dig("commit", "message").to_s.lines.first.to_s.strip,
        "date" => cm.dig("commit", "author", "date"),
        "url" => cm["html_url"],
      }
    end,
    "readme_html" => tidy_readme(
      api_get("/repos/#{OWNER}/#{repo}/readme", accept: "application/vnd.github.html"), repo, branch
    ),
  }
end

File.write(OUTPUT, JSON.pretty_generate(info))
puts "saved #{OUTPUT} (#{info.size} repos)"
